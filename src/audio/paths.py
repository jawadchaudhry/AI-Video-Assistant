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
    search_name = sanitize_name(source_name)
    base_dir = config.downloads_dir / search_name

    if not base_dir.exists():
        try:
            if config.downloads_dir.exists():
                for existing_dir in config.downloads_dir.iterdir():
                    if existing_dir.is_dir():
                        dir_name = existing_dir.name
                        if dir_name.startswith(search_name) or search_name.startswith(dir_name.split(" - ")[0] if " - " in dir_name else dir_name):
                            return existing_dir
        except Exception:
            pass

    return base_dir


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


def rename_download_folder(source_name: str, title: str) -> Path:
    """
    Rename downloads folder to include video title for better readability.

    Args:
        source_name: Original source identifier (e.g., 'youtube_Ty8gcCKuwNI')
        title: Video title to append

    Returns:
        Updated folder path with title appended.
    """
    config = get_config()

    safe_title = "".join(c for c in title[:20] if c.isalnum() or c in " -_").strip()
    new_folder_name = f"{source_name} - ({safe_title})"

    old_dir = config.downloads_dir / source_name
    new_dir = config.downloads_dir / new_folder_name

    if new_dir.exists():
        return new_dir

    if old_dir.exists() and old_dir != new_dir:
        import shutil
        new_dir.mkdir(parents=True, exist_ok=True)
        for item in old_dir.iterdir():
            shutil.move(str(item), str(new_dir))
        old_dir.rmdir()
        return new_dir

    if old_dir.exists():
        return old_dir

    return get_source_download_dir(source_name)
