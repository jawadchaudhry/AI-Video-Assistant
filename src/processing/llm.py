"""Shared LLM client configuration to eliminate duplicate code."""

import logging
import os
from functools import lru_cache
from typing import Optional

from langchain_mistralai import ChatMistralAI

from src.config import get_config

logger = logging.getLogger(__name__)


class LLMCapacityError(RuntimeError):
    """Raised when the configured Mistral model is temporarily unavailable."""


@lru_cache(maxsize=1)
def get_llm(temperature: Optional[float] = None) -> ChatMistralAI:
    """
    Get a singleton LLM instance using Mistral AI.

    Args:
        temperature: Override default temperature. Defaults to config value.

    Returns:
        Configured ChatMistralAI instance.

    Raises:
        EnvironmentError: If MISTRAL_API_KEY is not set.
    """
    config = get_config()

    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise EnvironmentError("MISTRAL_API_KEY environment variable is not set")

    model = config.llm_model

    logger.info(f"Initializing LLM with Mistral model: {model}")

    return ChatMistralAI(
        model=model,
        mistral_api_key=api_key,
        temperature=temperature if temperature is not None else config.llm_temperature,
        max_retries=3,
    )


def run_llm_with_capacity_guard(prompt_callable, *args, **kwargs):
    """Run an LLM call and normalize common provider capacity failures."""
    try:
        return prompt_callable(*args, **kwargs)
    except Exception as exc:
        message = str(exc).lower()
        if "service_tier_capacity_exceeded" in message or "capacity exceeded" in message:
            raise LLMCapacityError(
                "The configured Mistral model is temporarily at capacity. "
                "Set LLM_MODEL=mistral-tiny in your Space secrets or try again later."
            ) from exc
        raise
