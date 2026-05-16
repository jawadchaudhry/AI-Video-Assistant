"""Meeting information extractor for action items, decisions, and questions."""

import logging
from dataclasses import dataclass

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import get_config
from src.processing.llm import get_llm

logger = logging.getLogger(__name__)


ACTION_ITEMS_PROMPT = """
Extract action items from the meeting.

Return concise bullet points.

If none exist say:
No action items found.
"""

KEY_DECISIONS_PROMPT = """
Extract key decisions made.

Return concise bullet points.

If none exist say:
No key decisions found.
"""

OPEN_QUESTIONS_PROMPT = """
Extract unanswered/open questions.

Return concise bullet points.

If none exist say:
No open questions found.
"""


def _run_extraction(
    transcript: str,
    instruction: str,
    max_length: int = 12000,
) -> str:
    """Run a single extraction task with the LLM."""
    config = get_config()

    prompt = ChatPromptTemplate.from_messages([
        ("system", instruction),
        ("human", "{text}"),
    ])

    chain = prompt | get_llm() | StrOutputParser()

    truncated = transcript[:max_length]
    result = chain.invoke({"text": truncated})

    return result


def extract_action_items(transcript: str) -> str:
    """
    Extract action items from transcript.

    Args:
        transcript: Meeting transcript text.

    Returns:
        Extracted action items as formatted text.
    """
    logger.info("Extracting action items")
    return _run_extraction(transcript, ACTION_ITEMS_PROMPT)


def extract_key_decisions(transcript: str) -> str:
    """
    Extract key decisions from transcript.

    Args:
        transcript: Meeting transcript text.

    Returns:
        Extracted key decisions as formatted text.
    """
    logger.info("Extracting key decisions")
    return _run_extraction(transcript, KEY_DECISIONS_PROMPT)


def extract_questions(transcript: str) -> str:
    """
    Extract open/unanswered questions from transcript.

    Args:
        transcript: Meeting transcript text.

    Returns:
        Extracted questions as formatted text.
    """
    logger.info("Extracting open questions")
    return _run_extraction(transcript, OPEN_QUESTIONS_PROMPT)