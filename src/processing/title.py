"""Meeting title generator from transcript."""

import logging

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import get_config
from src.processing.llm import get_llm

logger = logging.getLogger(__name__)


def generate_title(transcript: str) -> str:
    """
    Generate a professional meeting title from transcript.

    Args:
        transcript: Meeting transcript text (truncated internally if needed).

    Returns:
        Generated meeting title (max ~8 words).
    """
    config = get_config()

    # Use first portion for title generation
    truncated = transcript[:config.max_title_length_chars]

    logger.info("Generating meeting title")

    title_chain = ChatPromptTemplate.from_messages([
        (
            "system",
            "Based on the meeting transcript, generate a short professional meeting title "
            "(max 8 words). Only return the title, nothing else.",
        ),
        ("human", "{text}"),
    ]) | get_llm() | StrOutputParser()

    result = title_chain.invoke({"text": truncated})

    logger.info(f"Title generated: {result}")
    return result.strip()