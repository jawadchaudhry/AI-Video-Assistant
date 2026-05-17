"""Cache management for transcripts and intermediate files."""

import hashlib
import logging
import time
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

    if not base_dir.exists():
        try:
            if config.cache_dir.exists():
                for existing_dir in config.cache_dir.iterdir():
                    if existing_dir.is_dir():
                        dir_name = existing_dir.name
                        if dir_name.startswith(source_id) or source_id.startswith(dir_name.split(" - ")[0] if " - " in dir_name else dir_name):
                            base_dir = existing_dir
                            break
        except Exception:
            pass

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


def rename_cache_folder(source_id: str, title: str) -> CachePaths:
    """
    Rename cache folder to include video title for better readability.

    Args:
        source_id: Original source identifier (e.g., 'youtube_Ty8gcCKuwNI')
        title: Video title to append

    Returns:
        Updated CachePaths object with new folder name.
    """
    config = get_config()

    safe_title = "".join(c for c in title[:20] if c.isalnum() or c in " -_").strip()
    new_folder_name = f"{source_id} - ({safe_title})"

    old_dir = config.cache_dir / source_id
    new_dir = config.cache_dir / new_folder_name

    if new_dir.exists():
        return CachePaths(
            base_dir=new_dir,
            transcript=new_dir / "transcript.txt",
            summary=new_dir / "summary.txt",
            chroma=new_dir / "chroma",
        )

    if old_dir.exists() and old_dir != new_dir:
        import shutil
        shutil.move(str(old_dir), str(new_dir))
        logger.info(f"Renamed cache folder to: {new_folder_name}")

    if old_dir.exists():
        return CachePaths(
            base_dir=old_dir,
            transcript=old_dir / "transcript.txt",
            summary=old_dir / "summary.txt",
            chroma=old_dir / "chroma",
        )

    paths = get_cache_paths(source_id)
    return CachePaths(
        base_dir=paths.base_dir,
        transcript=paths.base_dir / "transcript.txt",
        summary=paths.base_dir / "summary.txt",
        chroma=paths.base_dir / "chroma",
    )


def is_cache_stale(base_dir: Path) -> bool:
    """
    Check if cache directory is stale based on TTL.

    Args:
        base_dir: Cache directory path.

    Returns:
        True if cache is stale or doesn't exist, False otherwise.
    """
    if not base_dir.exists():
        return True

    config = get_config()
    cache_age_days = (time.time() - base_dir.stat().st_mtime) / 86400

    if cache_age_days > config.cache_ttl_days:
        logger.info(f"Cache stale: {cache_age_days:.1f} days old (TTL: {config.cache_ttl_days} days)")
        return True

    return False


def load_transcript(transcript_path: Path) -> str | None:
    """
    Load cached transcript if exists and not stale.

    Args:
        transcript_path: Path to transcript file.

    Returns:
        Transcript text or None if not found or stale.
    """
    if transcript_path.exists():
        config = get_config()
        cache_dir = transcript_path.parent

        if is_cache_stale(cache_dir):
            logger.info(f"Cache expired, removing: {transcript_path}")
            import shutil
            shutil.rmtree(cache_dir, ignore_errors=True)
            return None

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
