"""Helpers for organizing generated audio files under downloads."""

from __future__ import annotations

import re
from pathlib import Path

from src.config import get_config

_INVALID_CHARS = re.compile(r"[^A-Za-z0-9._-]+")
_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def sanitize_name(name: str) -> str:
    """Convert a title or filename into a safe Windows folder name."""
    cleaned = _INVALID_CHARS.sub("_", name.strip()).strip("._- ")
    if not cleaned:
        cleaned = "source"
    if cleaned.upper() in _RESERVED_NAMES:
        cleaned = f"_{cleaned}"
    return cleaned[:120]


def get_source_download_dir(source_name: str) -> Path:
    """Return the per-source folder inside the downloads directory."""
    config = get_config()
    return config.downloads_dir / sanitize_name(source_name)


def ensure_source_download_dir(source_name: str) -> Path:
    """Create and return the per-source download folder."""
    source_dir = get_source_download_dir(source_name)
    source_dir.mkdir(parents=True, exist_ok=True)
    return source_dir


def ensure_unique_source_download_dir(source_name: str) -> Path:
    """
    Create and return a collision-safe per-source download folder.

    If a folder with the same sanitized name already exists, append a numeric
    suffix to keep each source isolated.
    """
    config = get_config()
    base_name = sanitize_name(source_name)
    candidate = config.downloads_dir / base_name

    if not candidate.exists():
        candidate.mkdir(parents=True, exist_ok=True)
        return candidate

    for index in range(2, 1000):
        candidate = config.downloads_dir / f"{base_name}_{index}"
        if not candidate.exists():
            candidate.mkdir(parents=True, exist_ok=True)
            return candidate

    raise RuntimeError(f"Unable to create a unique downloads folder for: {source_name}")
