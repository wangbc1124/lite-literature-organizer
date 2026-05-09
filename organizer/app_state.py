from __future__ import annotations

from organizer.auto_organize import (
    catalog_rows,
    folder_rows,
    read_history_state,
    refresh_history_state,
    scan_inbox,
    settings_snapshot,
)
from organizer.i18n import category_labels_for


def inbox_payload(layout) -> dict:
    return {"items": scan_inbox(layout)}


def catalog_payload(layout) -> dict:
    return {"rows": catalog_rows(layout)}


def folder_payload(layout) -> dict:
    return {"folders": folder_rows(layout), "category_labels": category_labels_for(layout.locale)}


def settings_payload(layout) -> dict:
    return settings_snapshot(layout)


def history_payload(layout) -> dict:
    return {"events": read_history_state(layout)}


def refreshed_history_payload(layout) -> dict:
    return {"events": refresh_history_state(layout)}
