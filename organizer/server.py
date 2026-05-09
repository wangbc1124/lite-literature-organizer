from __future__ import annotations

import argparse
import json
import mimetypes
import socket
import traceback
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import os

from organizer.app_state import (
    catalog_payload,
    folder_payload,
    history_payload,
    inbox_payload,
    refreshed_history_payload,
    settings_payload,
)
from organizer.auto_organize import (
    apply_inbox_plan,
    ensure_layout,
    rebuild_catalog,
    refresh_history_state,
    resolve_root,
    scan_inbox,
)
from organizer.history_store import append_history, clear_history, delete_history_entry, state_file
from organizer.i18n import normalize_locale


STATIC_DIR = Path(__file__).resolve().parent / "web"


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


class OrganizeHandler(BaseHTTPRequestHandler):
    server_version = "LiteratureOrganizer/1.0"

    @property
    def app(self) -> "OrganizeHTTPServer":
        return self.server  # type: ignore[return-value]

    def log_message(self, format: str, *args) -> None:
        return

    def respond_json(self, payload: object, status: int = 200) -> None:
        body = json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def respond_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        content = path.read_bytes()
        mime_type, _ = mimetypes.guess_type(path.name)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", (mime_type or "application/octet-stream") + "; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def parse_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def request_locale(self, parsed) -> str:
        params = parse_qs(parsed.query)
        return normalize_locale(params.get("lang", [""])[0] or self.headers.get("X-Locale", ""))

    def do_GET(self) -> None:
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            locale = self.request_locale(parsed)

            if path == "/" or path == "/index.html":
                self.respond_file(STATIC_DIR / "index.html")
                return
            if path == "/app.js":
                self.respond_file(STATIC_DIR / "app.js")
                return
            if path == "/styles.css":
                self.respond_file(STATIC_DIR / "styles.css")
                return

            layout = ensure_layout(self.app.root, locale=locale)

            if path == "/api/inbox":
                self.respond_json(inbox_payload(layout))
                return
            if path == "/api/catalog":
                self.respond_json(catalog_payload(layout))
                return
            if path == "/api/folders":
                self.respond_json(folder_payload(layout))
                return
            if path == "/api/settings":
                self.respond_json(settings_payload(layout))
                return
            if path == "/api/history":
                self.respond_json(history_payload(layout))
                return

            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except Exception as exc:
            traceback.print_exc()
            self.respond_json({"error": str(exc), "type": exc.__class__.__name__}, status=500)

    def do_POST(self) -> None:
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            locale = self.request_locale(parsed)
            layout = ensure_layout(self.app.root, locale=locale)

            if path == "/api/inbox/scan":
                self.respond_json({"items": scan_inbox(layout)})
                return

            if path == "/api/inbox/apply":
                payload = self.parse_json_body()
                items = payload.get("items", [])
                if not isinstance(items, list):
                    self.respond_json({"error": "items must be a list"}, status=400)
                    return
                results = apply_inbox_plan(layout, items)
                refreshed_layout = ensure_layout(self.app.root, locale=locale)
                self.respond_json(
                    {
                        "results": results,
                        "items": inbox_payload(refreshed_layout)["items"],
                        "catalog_rows": catalog_payload(refreshed_layout)["rows"],
                    }
                )
                return

            if path == "/api/catalog/rebuild":
                self.parse_json_body()
                rows = rebuild_catalog(layout)
                refreshed_layout = ensure_layout(self.app.root, locale=locale)
                refresh_history_state(refreshed_layout)
                append_history(
                    refreshed_layout.app_root,
                    event_type="catalog_rebuild",
                    status="success",
                    detail="Rebuilt the literature catalog and refreshed managed folders.",
                )
                self.respond_json({"rows": rows, "folders": folder_payload(refreshed_layout)["folders"]})
                return

            if path == "/api/history/refresh":
                self.parse_json_body()
                refreshed_layout = ensure_layout(self.app.root, locale=locale)
                events = refreshed_history_payload(refreshed_layout)["events"]
                self.respond_json(
                    {
                        "events": events,
                        "rows": catalog_payload(refreshed_layout)["rows"],
                        "folders": folder_payload(refreshed_layout)["folders"],
                    }
                )
                return

            if path == "/api/history/delete":
                payload = self.parse_json_body()
                refreshed_layout = ensure_layout(self.app.root, locale=locale)
                entry_id = str(payload.get("id", "")).strip()
                clear_all = bool(payload.get("clear_all"))

                if clear_all:
                    clear_history(refreshed_layout.app_root)
                    self.respond_json({"ok": True, "events": []})
                    return

                if not entry_id:
                    self.respond_json({"error": "id is required"}, status=400)
                    return

                deleted = delete_history_entry(refreshed_layout.app_root, entry_id)
                if not deleted:
                    self.respond_json({"error": "history entry not found"}, status=404)
                    return

                self.respond_json({"ok": True, "events": history_payload(refreshed_layout)["events"]})
                return

            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except Exception as exc:
            traceback.print_exc()
            self.respond_json({"error": str(exc), "type": exc.__class__.__name__}, status=500)


class OrganizeHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], root: Path):
        super().__init__(server_address, OrganizeHandler)
        self.root = root


def find_available_port(host: str, preferred_port: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if sock.connect_ex((host, preferred_port)) != 0:
            return preferred_port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local literature organizer web app.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root directory for the literature workspace.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the local web server.")
    parser.add_argument("--port", type=int, default=8765, help="Preferred local port.")
    parser.add_argument("--open-browser", action="store_true", help="Open the app in the default browser.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = resolve_root(args.root)
    port = find_available_port(args.host, args.port)
    server = OrganizeHTTPServer((args.host, port), root)
    url = f"http://{args.host}:{port}"
    app_root = Path(__file__).resolve().parent
    app_root.mkdir(parents=True, exist_ok=True)
    state_file(app_root).write_text(
        json.dumps({"host": args.host, "port": port, "url": url, "pid": os.getpid()}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    append_history(
        app_root,
        event_type="service_start",
        status="success",
        detail=f"Local web service started at {url}.",
    )
    print(f"Literature organizer running at {url}")
    if args.open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
