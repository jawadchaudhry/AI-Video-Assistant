"""Meeting transcript summarizer using map-reduce pattern."""

import logging
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import get_config
from src.processing.llm import get_llm

logger = logging.getLogger(__name__)


def split_transcript(transcript: str, chunk_size: Optional[int] = None) -> list[str]:
    """Split transcript into chunks for parallel processing."""
    config = get_config()
    chunk_size = chunk_size or config.summary_chunk_size

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=config.summary_chunk_overlap,
    )

    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
    """
    Summarize a meeting transcript using map-reduce pattern.

    First maps chunks to partial summaries, then reduces to final summary.

    Args:
        transcript: Full meeting transcript text.

    Returns:
        Professional meeting summary.
    """
    logger.info(f"Summarizing transcript ({len(transcript)} chars)")

    map_prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize this portion of a meeting transcript concisely."),
        ("human", "{text}"),
    ])

    map_chain = map_prompt | get_llm() | StrOutputParser()

    chunks = split_transcript(transcript)
    logger.info(f"Processing {len(chunks)} chunks")

    chunk_summaries = [map_chain.invoke({"text": chunk}) for chunk in chunks]

    combined = "\n\n".join(chunk_summaries)

    reduce_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert meeting summarizer. Combine these partial summaries "
            "into one final professional meeting summary in bullet points.",
        ),
        ("human", "{text}"),
    ])

    reduce_chain = reduce_prompt | get_llm() | StrOutputParser()

    result = reduce_chain.invoke(combined)

    logger.info(f"Summary generated: {len(result)} chars")
    return result