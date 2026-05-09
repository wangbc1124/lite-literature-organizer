from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4


STATE_FILENAME = "server_state.json"
LOG_FILENAME = "organize_log.csv"
HISTORY_FILENAME = "history_log.jsonl"
SNAPSHOT_FILENAME = "workspace_snapshot.json"


def app_file(app_root: Path, filename: str) -> Path:
    return app_root / filename


def state_file(app_root: Path) -> Path:
    return app_file(app_root, STATE_FILENAME)


def log_file(app_root: Path) -> Path:
    return app_file(app_root, LOG_FILENAME)


def history_file(app_root: Path) -> Path:
    return app_file(app_root, HISTORY_FILENAME)


def snapshot_file(app_root: Path) -> Path:
    return app_file(app_root, SNAPSHOT_FILENAME)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def append_history(
    app_root: Path,
    *,
    event_type: str,
    source: str = "",
    before_path: str = "",
    after_path: str = "",
    status: str = "info",
    detail: str = "",
) -> dict:
    record = {
        "id": uuid4().hex,
        "timestamp": _now(),
        "event_type": event_type,
        "source": source,
        "before_path": before_path,
        "after_path": after_path,
        "status": status,
        "detail": detail,
    }
    path = history_file(app_root)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def _load_history_records(app_root: Path) -> list[dict]:
    path = history_file(app_root)
    if not path.exists():
        return []

    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            record.setdefault("id", f"legacy_{index}")
            rows.append(record)
    return rows


def read_history(app_root: Path, limit: int = 200) -> list[dict]:
    rows = _load_history_records(app_root)
    return rows[-limit:][::-1]


def clear_history(app_root: Path) -> None:
    history_file(app_root).write_text("", encoding="utf-8")


def delete_history_entry(app_root: Path, entry_id: str) -> bool:
    rows = _load_history_records(app_root)
    kept = [row for row in rows if row.get("id") != entry_id]
    if len(kept) == len(rows):
        return False

    path = history_file(app_root)
    with path.open("w", encoding="utf-8") as handle:
        for row in kept:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return True


def load_snapshot(app_root: Path) -> dict:
    path = snapshot_file(app_root)
    if not path.exists():
        return {"files": {}, "folders": {}, "captured_at": ""}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"files": {}, "folders": {}, "captured_at": ""}


def save_snapshot(app_root: Path, snapshot: dict) -> None:
    path = snapshot_file(app_root)
    payload = dict(snapshot)
    payload["captured_at"] = _now()
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_snapshot(*, file_rows: list[dict], folder_rows: list[dict]) -> dict:
    file_map = {row["filename"]: row["relative_path"] for row in file_rows}
    folder_map = {row["key"]: row["relative_path"] for row in folder_rows}
    return {"files": file_map, "folders": folder_map}


def detect_manual_changes(app_root: Path, snapshot: dict) -> list[dict]:
    previous = load_snapshot(app_root)
    previous_files = previous.get("files", {})
    previous_folders = previous.get("folders", {})
    current_files = snapshot.get("files", {})
    current_folders = snapshot.get("folders", {})

    if not previous_files and not previous_folders:
        save_snapshot(app_root, snapshot)
        return []

    events: list[dict] = []

    for filename, old_path in previous_files.items():
        if filename in current_files:
            new_path = current_files[filename]
            if new_path != old_path:
                events.append(
                    append_history(
                        app_root,
                        event_type="manual_change_detected",
                        source=filename,
                        before_path=old_path,
                        after_path=new_path,
                        status="moved",
                        detail="Detected file move or rename outside the app.",
                    )
                )
        else:
            events.append(
                append_history(
                    app_root,
                    event_type="manual_change_detected",
                    source=filename,
                    before_path=old_path,
                    after_path="",
                    status="removed",
                    detail="Detected file removal outside the app.",
                )
            )

    for filename, new_path in current_files.items():
        if filename not in previous_files:
            events.append(
                append_history(
                    app_root,
                    event_type="manual_change_detected",
                    source=filename,
                    before_path="",
                    after_path=new_path,
                    status="added",
                    detail="Detected new managed file outside the app.",
                )
            )

    for key, old_path in previous_folders.items():
        if key in current_folders:
            new_path = current_folders[key]
            if new_path != old_path:
                events.append(
                    append_history(
                        app_root,
                        event_type="manual_change_detected",
                        source=key,
                        before_path=old_path,
                        after_path=new_path,
                        status="folder_moved",
                        detail="Detected managed folder rename or relocation.",
                    )
                )
        else:
            events.append(
                append_history(
                    app_root,
                    event_type="manual_change_detected",
                    source=key,
                    before_path=old_path,
                    after_path="",
                    status="folder_missing",
                    detail="Managed folder marker is missing from the previous path.",
                )
            )

    for key, new_path in current_folders.items():
        if key not in previous_folders:
            events.append(
                append_history(
                    app_root,
                    event_type="manual_change_detected",
                    source=key,
                    before_path="",
                    after_path=new_path,
                    status="folder_added",
                    detail="Detected a newly discovered managed folder.",
                )
            )

    save_snapshot(app_root, snapshot)
    return events
