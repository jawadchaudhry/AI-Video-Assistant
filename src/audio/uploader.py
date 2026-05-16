"""Helpers for saving uploaded media into the app downloads directory."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.audio.paths import ensure_source_download_dir


@dataclass(frozen=True)
class UploadedFileResult:
    """Result returned after persisting an uploaded file."""

    path: Path
    already_exists: bool
    source_id: str


def get_uploaded_file_source_id(uploaded_file: Any) -> str:
    """Return the stable source id used for a local upload."""
    payload = _get_uploaded_bytes(uploaded_file)
    content_hash = hashlib.sha256(payload).hexdigest()[:12]
    return f"local_{content_hash}"


def uploaded_file_already_exists(uploaded_file: Any) -> bool:
    """Check whether the uploaded file already exists in downloads."""
    source_id = get_uploaded_file_source_id(uploaded_file)
    original_name = Path(getattr(uploaded_file, "name", "uploaded_media")).name
    suffix = Path(original_name).suffix or ".mp4"
    destination = ensure_source_download_dir(source_id) / f"{source_id}{suffix}"
    return destination.exists()


def _get_uploaded_bytes(uploaded_file: Any) -> bytes:
    """Read bytes from a Streamlit uploaded file or file-like object."""
    if hasattr(uploaded_file, "getbuffer"):
        return bytes(uploaded_file.getbuffer())
    if hasattr(uploaded_file, "read"):
        data = uploaded_file.read()
        return data if isinstance(data, bytes) else bytes(data)
    raise TypeError("Unsupported uploaded file object")


def save_uploaded_file(uploaded_file: Any) -> UploadedFileResult:
    """
    Persist an uploaded file under downloads/<stable-source-id>/.

    The folder and cache identity are derived from the file contents so the
    same video/audio file does not get uploaded or cached twice.
    """
    original_name = Path(getattr(uploaded_file, "name", "uploaded_media")).name
    original_path = Path(original_name)
    suffix = original_path.suffix or ".mp4"

    payload = _get_uploaded_bytes(uploaded_file)
    content_hash = hashlib.sha256(payload).hexdigest()[:12]
    source_id = f"local_{content_hash}"

    source_dir = ensure_source_download_dir(source_id)
    destination = source_dir / f"{source_id}{suffix}"

    if destination.exists():
        return UploadedFileResult(destination, True, source_id)

    destination.write_bytes(payload)
    return UploadedFileResult(destination, False, source_id)
