from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader

from organizer.history_store import (
    append_history,
    build_snapshot,
    detect_manual_changes,
    log_file,
    read_history,
    save_snapshot,
)
from organizer.i18n import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    category_labels_for,
    default_category_dirs_for,
    locale_bundle,
    localized_names_for,
    normalize_locale,
)

LOG_FILENAME = "organize_log.csv"
CATEGORY_MARKER = ".organize_category"

MAX_TITLE_WORDS = 18
MAX_FILENAME_STEM = 180

DAFOAM_KEYWORDS = (
    "dafoam",
    "adjoint in dafoam",
    "implementation of discrete adjoint in dafoam",
)
LEGACY_DAFOAM_STEMS = ()
FIML_KEYWORDS = (
    "field inversion",
    "f i m l",
    "fiml",
    "machine learning",
    "data-driven turbulence",
    "data driven turbulence",
    "symbolic regression",
    "embedded neural network",
    "turbulence modeling for separated flows",
)
ADJOINT_KEYWORDS = (
    "adjoint",
    "discrete adjoint",
    "gradient computation",
    "automatic differentiation",
    "optimization",
)
REPORT_KEYWORDS = (
    "technical report",
    "lecture",
    "introduction",
    "automatic differentiation",
)
BOOK_KEYWORDS = (
    "third edition",
    "turbulence modeling for cfd",
)

AUTHOR_BLACKLIST = {
    "abstract",
    "introduction",
    "contents",
    "journal",
    "article",
    "technical",
    "report",
    "school",
    "university",
    "physics",
    "fluids",
}


@dataclass
class ParsedPdf:
    source: Path
    title: str
    author: str
    year: str
    text: str
    first_page_text: str


@dataclass
class Decision:
    status: str
    target_rel: Path
    reason: str
    category_key: str
    confidence: str


@dataclass
class FolderLayout:
    root: Path
    app_root: Path
    locale: str
    inbox_dir: Path
    review_dir: Path
    catalog_file: Path
    category_dirs: dict[str, Path]
    discovered_markers: dict[str, list[Path]]

    def category(self, key: str) -> Path:
        return self.category_dirs[key]


def clean_whitespace(text: str) -> str:
    return " ".join((text or "").split())


def normalize_ascii(text: str) -> str:
    replacements = {
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\ufb00": "ff",
        "\ufb01": "fi",
        "\ufb02": "fl",
        "\ufb03": "ffi",
        "\ufb04": "ffl",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = text.encode("ascii", "ignore").decode("ascii")
    return clean_whitespace(text)


def slugify(text: str, *, max_length: int | None = None) -> str:
    text = normalize_ascii(text)
    text = text.replace("&", " and ")
    text = re.sub(r"[^A-Za-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    if max_length:
        text = text[:max_length].rstrip("_")
    return text or "untitled"


def ensure_pdf_filename(name: str) -> str:
    base = name[:-4] if name.lower().endswith(".pdf") else name
    base = slugify(base, max_length=MAX_FILENAME_STEM)
    return f"{base}.pdf"


def write_marker(dir_path: Path, key: str) -> None:
    marker_path = dir_path / CATEGORY_MARKER
    marker_path.write_text(f"{key}\n", encoding="utf-8")


def resolve_named_path(root: Path, names: list[str], preferred: str) -> Path:
    ordered = [preferred, *[name for name in names if name != preferred]]
    for name in ordered:
        candidate = root / name
        if candidate.exists():
            return candidate
    return root / preferred


def find_category_markers(root: Path) -> dict[str, list[Path]]:
    default_dirs = default_category_dirs_for(DEFAULT_LOCALE)
    discovered: dict[str, list[Path]] = {}
    for marker_path in root.rglob(CATEGORY_MARKER):
        try:
            key = marker_path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if key not in default_dirs:
            continue
        discovered.setdefault(key, []).append(marker_path.parent)
    return discovered


def discover_category_dirs(root: Path, discovered: dict[str, list[Path]], locale: str) -> dict[str, Path]:
    default_category_dirs = default_category_dirs_for(locale)
    resolved: dict[str, Path] = {}
    for key, default_rel in default_category_dirs.items():
        candidates = sorted(discovered.get(key, []), key=lambda path: (len(path.parts), path.as_posix()))
        resolved[key] = candidates[0] if candidates else root / default_rel
    return resolved


def ensure_layout(root: Path, app_root: Path | None = None, locale: str | None = None) -> FolderLayout:
    root = root.resolve()
    app_root = (app_root or Path(__file__).resolve().parent).resolve()
    locale = normalize_locale(locale)
    bundle = locale_bundle(locale)
    app_root.mkdir(parents=True, exist_ok=True)
    inbox_dir = resolve_named_path(root, localized_names_for("inbox"), bundle["inbox_dirname"])
    review_dir = resolve_named_path(root, localized_names_for("review"), bundle["review_dirname"])
    catalog_file = resolve_named_path(root, localized_names_for("catalog"), bundle["catalog_filename"])
    inbox_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    discovered = find_category_markers(root)
    category_dirs = discover_category_dirs(root, discovered, locale)
    for key, path in category_dirs.items():
        path.mkdir(parents=True, exist_ok=True)
        marker_path = path / CATEGORY_MARKER
        if not marker_path.exists():
            write_marker(path, key)

    discovered = find_category_markers(root)
    category_dirs = discover_category_dirs(root, discovered, locale)
    return FolderLayout(
        root=root,
        app_root=app_root,
        locale=locale,
        inbox_dir=inbox_dir,
        review_dir=review_dir,
        catalog_file=catalog_file,
        category_dirs=category_dirs,
        discovered_markers=discovered,
    )


def extract_pdf_text(pdf_path: Path) -> tuple[str, str]:
    reader = PdfReader(str(pdf_path), strict=False)
    first_page = ""
    text_parts: list[str] = []
    for index, page in enumerate(reader.pages[:2]):
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        if index == 0:
            first_page = page_text
        text_parts.append(page_text[:10000])
    return "\n".join(text_parts), first_page


def parse_pdf(pdf_path: Path) -> ParsedPdf:
    reader = PdfReader(str(pdf_path), strict=False)
    metadata = reader.metadata or {}
    text, first_page = extract_pdf_text(pdf_path)
    first_page_ascii = "\n".join(normalize_ascii(line) for line in first_page.splitlines())
    full_text_ascii = normalize_ascii(text)

    title = extract_title(metadata, first_page_ascii, pdf_path)
    author = extract_author(metadata, first_page_ascii, pdf_path, title)
    year = extract_year(metadata, full_text_ascii)
    return ParsedPdf(
        source=pdf_path,
        title=title,
        author=author,
        year=year,
        text=full_text_ascii.lower(),
        first_page_text=first_page_ascii,
    )


def extract_title(metadata: dict, first_page_text: str, pdf_path: Path) -> str:
    meta_title = normalize_ascii(clean_whitespace(str(metadata.get("/Title", ""))))
    if is_good_title(meta_title):
        return meta_title

    lines = [clean_whitespace(line) for line in first_page_text.splitlines()]
    candidate_lines: list[str] = []
    for line in lines[:20]:
        ascii_line = normalize_ascii(line)
        if not ascii_line:
            continue
        lower_line = ascii_line.lower()
        if any(token in lower_line for token in ("abstract", "contents", "journal", "received", "doi")):
            continue
        if re.search(r"\b(university|school of|department of|institute)\b", lower_line):
            continue
        if len(ascii_line.split()) < 3:
            continue
        candidate_lines.append(ascii_line)
        if len(candidate_lines) >= 3:
            break

    if candidate_lines:
        title = " ".join(candidate_lines[:2])
        title = re.split(r"\b(Abstract|Contents)\b", title, maxsplit=1)[0]
        title = clean_whitespace(title)
        if is_good_title(title):
            return title

    return normalize_ascii(pdf_path.stem)


def is_good_title(title: str) -> bool:
    if not title:
        return False
    lower = title.lower()
    if re.match(r"^[A-Za-z]:/", title):
        return False
    if len(title.split()) < 3:
        return False
    if lower in AUTHOR_BLACKLIST:
        return False
    return True


def extract_author(metadata: dict, first_page_text: str, pdf_path: Path, title_hint: str) -> str:
    meta_author = normalize_ascii(clean_whitespace(str(metadata.get("/Author", ""))))
    author = choose_first_author(meta_author)
    if author:
        return author

    title_lower = title_hint.lower()
    lines = [normalize_ascii(clean_whitespace(line)) for line in first_page_text.splitlines()]
    for line in lines[:20]:
        line_lower = line.lower()
        if line_lower and (line_lower in title_lower or title_lower in line_lower):
            continue
        author = choose_first_author(line)
        if author:
            return author

    stem_tokens = [token for token in re.split(r"[^A-Za-z]+", pdf_path.stem) if token]
    return stem_tokens[0].title() if stem_tokens else ""


def choose_first_author(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r"\([^)]*\)", " ", text)
    cleaned = re.sub(r"\b(and|with)\b", ",", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[*\d]+", " ", cleaned)
    segments = [clean_whitespace(seg) for seg in cleaned.split(",") if clean_whitespace(seg)]
    for seg in segments:
        words = seg.split()
        if not 1 < len(words) <= 4:
            continue
        if any(word.lower() in AUTHOR_BLACKLIST for word in words):
            continue
        alpha_words = [word for word in words if re.search(r"[A-Za-z]", word)]
        if len(alpha_words) < 2:
            continue
        surname = re.sub(r"[^A-Za-z-]", "", alpha_words[-1])
        if surname:
            return surname.title()
    return ""


def extract_year(metadata: dict, text: str) -> str:
    match = re.search(r"\b(19|20)\d{2}\b", text[:5000])
    if match:
        return match.group(0)
    for key in ("/CreationDate", "/ModDate"):
        raw = str(metadata.get(key, ""))
        match = re.search(r"(19|20)\d{2}", raw)
        if match:
            return match.group(0)
    return "n.d."


def looks_like_book(parsed: ParsedPdf, merged: str) -> bool:
    if any(keyword in merged for keyword in BOOK_KEYWORDS):
        return True
    return len(parsed.first_page_text.split()) < 8 and parsed.source.stem.lower().startswith("turbulence modeling for cfd")


def looks_like_report(parsed: ParsedPdf, merged: str) -> bool:
    if "dafoam" in merged and "introduction" in merged:
        return True
    return any(keyword in merged for keyword in REPORT_KEYWORDS) and "journal" not in merged


def confidence_for_reason(reason: str) -> str:
    if reason in {"dafoam_match", "book_match", "report_match"}:
        return "high"
    if reason in {"fiml_match", "adjoint_match"}:
        return "medium"
    if reason == "default_other":
        return "low"
    return "review"


def classify_article(parsed: ParsedPdf, merged: str, layout: FolderLayout) -> tuple[Path, str, str]:
    if any(keyword in merged for keyword in DAFOAM_KEYWORDS):
        return layout.category("dafoam"), "dafoam_match", "dafoam"
    if any(keyword in merged for keyword in FIML_KEYWORDS):
        return layout.category("fiml"), "fiml_match", "fiml"
    if any(keyword in merged for keyword in ADJOINT_KEYWORDS):
        return layout.category("adjoint"), "adjoint_match", "adjoint"
    return layout.category("other"), "default_other", "other"


def classify(parsed: ParsedPdf, layout: FolderLayout) -> Decision:
    title_lower = parsed.title.lower()
    merged = f"{title_lower} {parsed.text}"

    if not is_good_title(parsed.title) or not parsed.author or not parsed.year:
        return Decision(
            status="needs_review",
            target_rel=layout.review_dir.relative_to(layout.root) / parsed.source.name,
            reason="missing_title_author_or_year",
            category_key="review",
            confidence="review",
        )

    if looks_like_book(parsed, merged):
        target_dir = layout.category("book")
        reason = "book_match"
        category_key = "book"
    elif looks_like_report(parsed, merged):
        target_dir = layout.category("report")
        reason = "report_match"
        category_key = "report"
    else:
        target_dir, reason, category_key = classify_article(parsed, merged, layout)

    return Decision(
        status="organized",
        target_rel=target_dir.relative_to(layout.root) / build_filename(parsed),
        reason=reason,
        category_key=category_key,
        confidence=confidence_for_reason(reason),
    )


def build_filename(parsed: ParsedPdf) -> str:
    title_words = normalize_ascii(parsed.title).split()
    if len(title_words) > MAX_TITLE_WORDS:
        title_words = title_words[:MAX_TITLE_WORDS]
    title = slugify(" ".join(title_words))
    author = slugify(parsed.author, max_length=40)
    stem = f"{parsed.year}_{author}_{title}"
    if len(stem) > MAX_FILENAME_STEM:
        stem = stem[:MAX_FILENAME_STEM].rstrip("_")
    return f"{stem}.pdf"


def summarize_excerpt(text: str, limit: int = 260) -> str:
    compact = clean_whitespace(text)
    return compact[:limit].rstrip() if len(compact) <= limit else compact[: limit - 3].rstrip() + "..."


def decision_to_candidate(parsed: ParsedPdf, decision: Decision, layout: FolderLayout) -> dict:
    target_path = layout.root / decision.target_rel
    category_labels = category_labels_for(layout.locale)
    return {
        "source_name": parsed.source.name,
        "source_rel": parsed.source.relative_to(layout.root).as_posix(),
        "title": parsed.title,
        "author": parsed.author,
        "year": parsed.year,
        "reason": decision.reason,
        "confidence": decision.confidence,
        "status": decision.status,
        "category_key": decision.category_key,
        "category_label": category_labels.get(decision.category_key, decision.category_key),
        "target_rel": decision.target_rel.as_posix(),
        "target_dir_rel": target_path.parent.relative_to(layout.root).as_posix(),
        "proposed_filename": target_path.name,
        "excerpt": summarize_excerpt(parsed.first_page_text),
        "target_exists": target_path.exists(),
    }


def scan_inbox(layout: FolderLayout) -> list[dict]:
    results: list[dict] = []
    category_labels = category_labels_for(layout.locale)
    for pdf_path in sorted(layout.inbox_dir.glob("*.pdf")):
        try:
            parsed = parse_pdf(pdf_path)
            decision = classify(parsed, layout)
            candidate = decision_to_candidate(parsed, decision, layout)
        except Exception as exc:
            rel = (layout.review_dir.relative_to(layout.root) / pdf_path.name).as_posix()
            candidate = {
                "source_name": pdf_path.name,
                "source_rel": pdf_path.relative_to(layout.root).as_posix(),
                "title": normalize_ascii(pdf_path.stem),
                "author": "",
                "year": "n.d.",
                "reason": f"parse_error:{exc.__class__.__name__}",
                "confidence": "review",
                "status": "failed_parse",
                "category_key": "review",
                "category_label": category_labels["review"],
                "target_rel": rel,
                "target_dir_rel": layout.review_dir.relative_to(layout.root).as_posix(),
                "proposed_filename": pdf_path.name,
                "excerpt": "PDF parse failed. Review manually.",
                "target_exists": (layout.review_dir / pdf_path.name).exists(),
            }
        results.append(candidate)
    return results


def append_log(app_root: Path, rows: Iterable[tuple[str, str, str, str, str]]) -> None:
    log_path = log_file(app_root)
    new_file = not log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        if new_file:
            writer.writerow(["timestamp", "source_name", "target_path", "status", "reason"])
        writer.writerows(rows)


def catalog_rows(layout: FolderLayout) -> list[dict]:
    inbox_name = layout.inbox_dir.relative_to(layout.root).parts[0]
    rows: list[dict] = []
    for pdf_path in sorted(layout.root.rglob("*.pdf")):
        rel = pdf_path.relative_to(layout.root)
        if rel.parts and rel.parts[0] == inbox_name:
            continue
        rows.append(
            {
                "stem": pdf_path.stem,
                "filename": pdf_path.name,
                "relative_path": rel.as_posix(),
                "parent_dir": rel.parent.as_posix() if rel.parent != Path(".") else "",
                "top_level": rel.parts[0] if rel.parts else "",
                "subfolders": " / ".join(rel.parts[1:-1]),
            }
        )
    return rows


def rebuild_catalog(layout: FolderLayout) -> list[dict]:
    rows = catalog_rows(layout)
    with layout.catalog_file.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(["stem", "filename", "relative_path", "parent_dir", "top_level", "subfolders"])
        for row in rows:
            writer.writerow(
                [
                    row["stem"],
                    row["filename"],
                    row["relative_path"],
                    row["parent_dir"],
                    row["top_level"],
                    row["subfolders"],
                ]
            )
    return rows


def folder_rows(layout: FolderLayout) -> list[dict]:
    category_labels = category_labels_for(layout.locale)
    default_category_dirs = default_category_dirs_for(layout.locale)
    rows: list[dict] = []
    for key in default_category_dirs:
        active = layout.category(key)
        duplicates = [
            marker_dir.relative_to(layout.root).as_posix()
            for marker_dir in layout.discovered_markers.get(key, [])
            if marker_dir != active
        ]
        rows.append(
            {
                "key": key,
                "label": category_labels.get(key, key),
                "relative_path": active.relative_to(layout.root).as_posix(),
                "marker_file": (active / CATEGORY_MARKER).relative_to(layout.root).as_posix(),
                "duplicates": duplicates,
                "source": "discovered" if key in layout.discovered_markers else "default_rebuilt",
            }
        )
    rows.append(
        {
            "key": "review",
            "label": category_labels["review"],
            "relative_path": layout.review_dir.relative_to(layout.root).as_posix(),
            "marker_file": "",
            "duplicates": [],
            "source": "fixed",
        }
    )
    return rows


def workspace_snapshot(layout: FolderLayout) -> dict:
    return build_snapshot(file_rows=catalog_rows(layout), folder_rows=folder_rows(layout))


def record_history_event(
    layout: FolderLayout,
    *,
    event_type: str,
    source: str = "",
    before_path: str = "",
    after_path: str = "",
    status: str = "info",
    detail: str = "",
) -> dict:
    return append_history(
        layout.app_root,
        event_type=event_type,
        source=source,
        before_path=before_path,
        after_path=after_path,
        status=status,
        detail=detail,
    )


def refresh_history_state(layout: FolderLayout) -> list[dict]:
    detect_manual_changes(layout.app_root, workspace_snapshot(layout))
    return read_history(layout.app_root)


def read_history_state(layout: FolderLayout) -> list[dict]:
    return read_history(layout.app_root)


def sync_history_state(layout: FolderLayout) -> None:
    save_snapshot(layout.app_root, workspace_snapshot(layout))


def settings_snapshot(layout: FolderLayout) -> dict:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    bundle = locale_bundle(layout.locale)
    return {
        "root": str(layout.root),
        "app_root": str(layout.app_root),
        "current_locale": layout.locale,
        "supported_locales": list(SUPPORTED_LOCALES),
        "default_locale_source": "localStorage_then_browser_then_en",
        "current_locale_behavior": "existing_dirs_preserved_new_defaults_follow_locale",
        "inbox_dir": layout.inbox_dir.relative_to(layout.root).as_posix(),
        "review_dir": layout.review_dir.relative_to(layout.root).as_posix(),
        "catalog_file": layout.catalog_file.name,
        "log_file": log_file(layout.app_root).name,
        "history_file": "history_log.jsonl",
        "launcher_script": bundle["launcher_script"],
        "gpt_configured": bool(api_key),
        "gpt_enabled": False,
        "gpt_status": "disabled_no_api" if not api_key else "disabled_not_implemented",
        "manual_compatibility": "folders can be renamed or moved as long as .organize_category stays with managed folders",
    }


def apply_inbox_plan(layout: FolderLayout, entries: list[dict]) -> list[dict]:
    results: list[dict] = []
    log_rows: list[tuple[str, str, str, str, str]] = []

    for entry in entries:
        source_name = str(entry.get("source_name", "")).strip()
        category_key = str(entry.get("category_key", "")).strip() or "review"
        requested_filename = str(entry.get("filename", "")).strip()
        source_path = layout.inbox_dir / source_name
        timestamp = datetime.now().isoformat(timespec="seconds")

        if not source_name or not source_path.exists():
            results.append(
                {
                    "source_name": source_name,
                    "status": "missing_source",
                    "reason": "source_not_found",
                }
            )
            continue

        if category_key == "review":
            target_dir = layout.review_dir
        elif category_key in layout.category_dirs:
            target_dir = layout.category(category_key)
        else:
            results.append(
                {
                    "source_name": source_name,
                    "status": "invalid_category",
                    "reason": f"unknown_category:{category_key}",
                }
            )
            continue

        filename = ensure_pdf_filename(requested_filename or source_name)
        target_path = target_dir / filename

        if target_path.exists():
            result = {
                "source_name": source_name,
                "status": "skipped_exists",
                "reason": "target_exists",
                "target_rel": target_path.relative_to(layout.root).as_posix(),
            }
            results.append(result)
            log_rows.append((timestamp, source_name, result["target_rel"], "skipped_exists", "target_exists"))
            record_history_event(
                layout,
                event_type="apply_one",
                source=source_name,
                before_path=source_path.relative_to(layout.root).as_posix(),
                after_path=result["target_rel"],
                status="skipped_exists",
                detail="Target file already exists. No changes were applied.",
            )
            continue

        shutil.move(str(source_path), str(target_path))
        result = {
            "source_name": source_name,
            "status": "applied",
            "reason": "applied",
            "target_rel": target_path.relative_to(layout.root).as_posix(),
        }
        results.append(result)
        log_rows.append((timestamp, source_name, result["target_rel"], "applied", "applied"))
        record_history_event(
            layout,
            event_type="apply_one",
            source=source_name,
            before_path=source_path.relative_to(layout.root).as_posix(),
            after_path=result["target_rel"],
            status="applied",
            detail=f"Moved file into category '{category_key}'.",
        )

    if log_rows:
        append_log(layout.app_root, log_rows)
    rebuild_catalog(layout)
    sync_history_state(layout)
    return results


def process_inbox(layout: FolderLayout, *, dry_run: bool = False) -> int:
    candidates = scan_inbox(layout)
    if not candidates:
        print(f"No PDF files found in {layout.inbox_dir.name}.")
        if not dry_run:
            rebuild_catalog(layout)
        return 0

    log_rows: list[tuple[str, str, str, str, str]] = []
    for candidate in candidates:
        timestamp = datetime.now().isoformat(timespec="seconds")
        source_name = candidate["source_name"]
        target_rel = candidate["target_rel"]
        reason = candidate["reason"]
        target_path = layout.root / Path(target_rel)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if candidate["target_exists"]:
            status = "skipped_exists"
            reason = "target_exists"
            print(f"[SKIP] {source_name} -> {target_rel} ({reason})")
        else:
            status = candidate["status"]
            if dry_run:
                print(f"[DRY RUN] {source_name} -> {target_rel} ({reason})")
            else:
                shutil.move(str(layout.inbox_dir / source_name), str(target_path))
                print(f"[OK] {source_name} -> {target_rel} ({reason})")
        log_rows.append((timestamp, source_name, target_rel, status, reason))

    if not dry_run:
        append_log(layout.app_root, log_rows)
        rebuild_catalog(layout)
        for _, source_name, target_rel, status, reason in log_rows:
            record_history_event(
                layout,
                event_type="apply_batch",
                source=source_name,
                before_path=(layout.inbox_dir / source_name).relative_to(layout.root).as_posix(),
                after_path=target_rel,
                status=status,
                detail=reason,
            )
        sync_history_state(layout)
    return 0


def reclassify_dafoam(layout: FolderLayout, *, dry_run: bool = False) -> int:
    moved = 0
    fiml_dir = layout.category("fiml")
    dafoam_dir = layout.category("dafoam")
    for pdf_path in sorted(fiml_dir.glob("*.pdf")):
        try:
            parsed = parse_pdf(pdf_path)
        except Exception:
            continue
        merged = f"{parsed.title.lower()} {parsed.text}"
        if not (any(keyword in merged for keyword in DAFOAM_KEYWORDS) or pdf_path.stem in LEGACY_DAFOAM_STEMS):
            continue
        target = dafoam_dir / pdf_path.name
        if target.exists():
            print(f"[SKIP] {pdf_path.name} -> {target.relative_to(layout.root).as_posix()} (target_exists)")
            continue
        moved += 1
        if dry_run:
            print(f"[DRY RUN] {pdf_path.name} -> {target.relative_to(layout.root).as_posix()} (reclassify_dafoam)")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(pdf_path), str(target))
            print(f"[OK] {pdf_path.name} -> {target.relative_to(layout.root).as_posix()} (reclassify_dafoam)")
    if moved == 0:
        print("No existing FIML PDFs matched DAFoam reclassification.")
    elif not dry_run:
        rebuild_catalog(layout)
        sync_history_state(layout)
    return 0


def resolve_root(path: Path) -> Path:
    return path.resolve() if path.exists() else path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organize PDFs from the configured inbox into the current literature root.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root directory for the literature workspace.")
    parser.add_argument("--lang", choices=list(SUPPORTED_LOCALES), default=DEFAULT_LOCALE, help="Locale for default names.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without moving files.")
    parser.add_argument(
        "--reclassify-dafoam",
        action="store_true",
        help="Re-scan existing FIML PDFs and move DAFoam-related ones into the DAFoam subfolder.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    layout = ensure_layout(resolve_root(args.root), locale=args.lang)
    if args.reclassify_dafoam:
        return reclassify_dafoam(layout, dry_run=args.dry_run)
    return process_inbox(layout, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
