"""Configuration and environment management for AI Video Assistant."""

import os
from pathlib import Path
from dataclasses import dataclass, field

# Load .env file at module import time
from dotenv import load_dotenv
load_dotenv()


@dataclass
class AppConfig:
    """Application configuration with validated settings."""

    # Application paths
    project_root: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    cache_dir: Path = field(init=False)
    downloads_dir: Path = field(init=False)
    hf_home: Path = field(init=False)

    # Whisper settings
    whisper_model: str = "tiny"
    whisper_device: str = "cpu"
    whisper_compute_type: str = "int8"
    whisper_beam_size: int = 5

    # Audio processing settings
    audio_chunk_seconds: int = 300
    audio_sample_rate: int = 16000
    audio_channels: int = 1

    # LLM settings
    llm_model: str = "mistral-tiny"
    llm_temperature: float = 0.3

    # Embedding settings
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_device: str = "cpu"

    # RAG settings
    rag_chunk_size: int = 300
    rag_chunk_overlap: int = 50
    rag_retriever_k: int = 6
    rag_retriever_fetch_k: int = 10
    rag_search_type: str = "mmr"

    # Processing settings
    summary_chunk_size: int = 3000
    summary_chunk_overlap: int = 200
    max_transcript_length: int = 12000
    max_title_length_chars: int = 2000

    # Cache settings
    cache_ttl_days: int = 7

    def __post_init__(self):
        """Set computed paths and load environment variables."""
        self.cache_dir = self._resolve_path("CACHE_DIR", self.project_root / "cache")
        self.downloads_dir = self._resolve_path("DOWNLOADS_DIR", self.project_root / "downloads")
        self.hf_home = self._resolve_path("HF_HOME", self.project_root / "hf_cache")

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.hf_home.mkdir(parents=True, exist_ok=True)

        # Override with env vars if present
        self.llm_model = os.getenv("LLM_MODEL", self.llm_model)
        self.whisper_model = os.getenv("WHISPER_MODEL", self.whisper_model)
        self.embedding_model = os.getenv("EMBEDDING_MODEL", self.embedding_model)

    def _resolve_path(self, env_var: str, default_path: Path) -> Path:
        """Resolve a configurable path from the environment."""
        raw_value = os.getenv(env_var)
        if not raw_value:
            return default_path

        resolved = Path(raw_value).expanduser()
        if not resolved.is_absolute():
            resolved = self.project_root / resolved
        return resolved

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if not os.getenv("MISTRAL_API_KEY"):
            errors.append("MISTRAL_API_KEY environment variable is not set")

        if self.whisper_model not in ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]:
            errors.append(f"Invalid WHISPER_MODEL: {self.whisper_model}")

        if self.llm_temperature < 0 or self.llm_temperature > 2:
            errors.append(f"LLM temperature must be between 0 and 2, got {self.llm_temperature}")

        return errors


# Global config instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get the global configuration instance."""
    return config


def validate_environment() -> None:
    """Validate environment and raise exception if invalid."""
    errors = config.validate()
    if errors:
        raise EnvironmentError(
            f"Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        )
