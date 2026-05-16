"""Cache management for transcripts and intermediate files."""

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from src.config import get_config

logger = logging.getLogger(__name__)


@dataclass
class CachePaths:
    """Container for cache paths for a specific source."""
    base_dir: Path
    transcript: Path
    summary: Path
    chroma: Path


def get_youtube_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from various URL formats.

    Args:
        url: YouTube URL.

    Returns:
        Video ID if found, None otherwise.
    """
    parsed = urlparse(url)

    if parsed.hostname in ["youtu.be"]:
        return parsed.path[1:]

    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]

    return None


def _hash_file_contents(file_path: Path) -> str:
    """Return a stable content hash for a file."""
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:12]


def generate_local_file_hash(file_path: str) -> str:
    """
    Generate stable hash for local files based on file contents.

    Args:
        file_path: Path to local file.

    Returns:
        12-character hash string.
    """
    return _hash_file_contents(Path(file_path))


def generate_source_id(source: str) -> str:
    """
    Create unique cache identifier for a source.

    Args:
        source: YouTube URL or local file path.

    Returns:
        Cache ID string (e.g., 'youtube_abc123' or 'local_def456')
    """
    if source.startswith("http"):
        video_id = get_youtube_video_id(source)
        if video_id:
            return f"youtube_{video_id}"

        # Fallback for non-standard URLs
        return f"url_{hashlib.md5(source.encode()).hexdigest()[:12]}"

    local_hash = generate_local_file_hash(source)
    return f"local_{local_hash}"


def get_cache_paths(source_id: str) -> CachePaths:
    """
    Get cache paths for a specific source.

    Args:
        source_id: Unique source identifier.

    Returns:
        CachePaths object with all relevant paths.
    """
    config = get_config()
    base_dir = config.cache_dir / source_id

    return CachePaths(
        base_dir=base_dir,
        transcript=base_dir / "transcript.txt",
        summary=base_dir / "summary.txt",
        chroma=base_dir / "chroma",
    )


def ensure_cache_dir(source_id: str) -> CachePaths:
    """
    Ensure cache directory exists and return paths.

    Args:
        source_id: Unique source identifier.

    Returns:
        CachePaths object with created directories.
    """
    paths = get_cache_paths(source_id)
    paths.base_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Cache directory: {paths.base_dir}")
    return paths


def load_transcript(transcript_path: Path) -> str | None:
    """
    Load cached transcript if exists.

    Args:
        transcript_path: Path to transcript file.

    Returns:
        Transcript text or None if not found.
    """
    if transcript_path.exists():
        logger.info(f"Loading cached transcript: {transcript_path}")
        return transcript_path.read_text(encoding="utf-8")
    return None


def save_transcript(transcript: str, transcript_path: Path) -> None:
    """
    Save transcript to cache.

    Args:
        transcript: Transcript text.
        transcript_path: Path to save to.
    """
    logger.info(f"Saving transcript: {transcript_path}")
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    transcript_path.write_text(transcript, encoding="utf-8")
