from __future__ import annotations

from pathlib import Path


SUPPORTED_LOCALES = ("zh-CN", "en")
DEFAULT_LOCALE = "en"


I18N = {
    "zh-CN": {
        "inbox_dirname": "收件箱",
        "review_dirname": "待确认",
        "catalog_filename": "文献总表.csv",
        "launcher_script": "organize.bat",
        "category_labels": {
            "book": "书籍",
            "report": "报告",
            "fiml": "FIML",
            "dafoam": "DAFoam",
            "adjoint": "离散伴随",
            "other": "其他",
            "review": "待确认",
        },
        "default_category_dirs": {
            "report": Path("报告"),
            "book": Path("书籍"),
            "fiml": Path("文章") / "FIML",
            "dafoam": Path("文章") / "DAFoam",
            "adjoint": Path("文章") / "离散伴随",
            "other": Path("文章") / "其他",
        },
    },
    "en": {
        "inbox_dirname": "inbox",
        "review_dirname": "review",
        "catalog_filename": "catalog.csv",
        "launcher_script": "organize.bat",
        "category_labels": {
            "book": "Books",
            "report": "Reports",
            "fiml": "FIML",
            "dafoam": "DAFoam",
            "adjoint": "Adjoint",
            "other": "Other",
            "review": "Review",
        },
        "default_category_dirs": {
            "report": Path("library") / "reports",
            "book": Path("library") / "books",
            "fiml": Path("library") / "articles" / "fiml",
            "dafoam": Path("library") / "articles" / "dafoam",
            "adjoint": Path("library") / "articles" / "adjoint",
            "other": Path("library") / "articles" / "other",
        },
    },
}


def normalize_locale(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE
    lowered = locale.strip().lower()
    if lowered.startswith("zh"):
        return "zh-CN"
    return "en"


def locale_bundle(locale: str | None) -> dict:
    return I18N[normalize_locale(locale)]


def category_labels_for(locale: str | None) -> dict[str, str]:
    return dict(locale_bundle(locale)["category_labels"])


def default_category_dirs_for(locale: str | None) -> dict[str, Path]:
    return dict(locale_bundle(locale)["default_category_dirs"])


def localized_names_for(kind: str) -> list[str]:
    values: list[str] = []
    for locale in SUPPORTED_LOCALES:
        bundle = locale_bundle(locale)
        if kind in {"inbox", "review"}:
            values.append(bundle[f"{kind}_dirname"])
        else:
            values.append(bundle["catalog_filename"])
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped
