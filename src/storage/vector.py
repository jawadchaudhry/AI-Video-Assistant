"""Vector store and RAG chain for semantic search."""

import logging
from pathlib import Path
from typing import Optional

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import get_config
from src.processing.llm import get_llm

logger = logging.getLogger(__name__)


def get_embeddings() -> HuggingFaceEmbeddings:
    """Get embedding model instance."""
    config = get_config()
    return HuggingFaceEmbeddings(
        model_name=config.embedding_model,
        model_kwargs={"device": config.embedding_device},
    )


def build_vector_store(transcript: str, persist_directory: Path) -> Chroma:
    """
    Create a new vector store from transcript.

    Args:
        transcript: Full transcript text.
        persist_directory: Directory to save ChromaDB.

    Returns:
        Configured Chroma vector store.
    """
    config = get_config()

    logger.info(f"Creating ChromaDB at {persist_directory}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.rag_chunk_size,
        chunk_overlap=config.rag_chunk_overlap,
    )

    chunks = splitter.split_text(transcript)

    docs = [
        Document(page_content=chunk, metadata={"chunk": i})
        for i, chunk in enumerate(chunks)
    ]

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=get_embeddings(),
        persist_directory=str(persist_directory),
        collection_name="meeting_transcript",
    )

    logger.info(f"Created vector store with {len(docs)} chunks")
    return vector_store


def load_vector_store(persist_directory: Path) -> Chroma:
    """
    Load existing vector store.

    Args:
        persist_directory: Directory containing ChromaDB.

    Returns:
        Loaded Chroma vector store.
    """
    logger.info(f"Loading existing ChromaDB from {persist_directory}")

    return Chroma(
        persist_directory=str(persist_directory),
        embedding_function=get_embeddings(),
        collection_name="meeting_transcript",
    )


def build_or_load_vector_store(transcript: str, persist_directory: Path) -> Chroma:
    """
    Build new or load existing vector store.

    Args:
        transcript: Full transcript text.
        persist_directory: Directory for ChromaDB.

    Returns:
        Vector store instance.
    """
    if persist_directory.exists() and any(persist_directory.iterdir()):
        return load_vector_store(persist_directory)

    return build_vector_store(transcript, persist_directory)


def format_docs(docs: list[Document]) -> str:
    """Format retrieved documents for prompt."""
    return "\n\n".join(doc.page_content for doc in docs)


RAG_SYSTEM_PROMPT = """
You are an expert AI meeting assistant.

RULES:
- Answer ONLY from transcript context
- If answer is missing say:
  'Not mentioned in meeting transcript'
- Be concise and accurate

CONTEXT:
{context}
"""


def create_rag_chain(transcript: str, chroma_path: Path):
    """
    Create a RAG chain for question answering.

    Args:
        transcript: Full transcript text.
        chroma_path: Path to ChromaDB.

    Returns:
        Runnable RAG chain.
    """
    config = get_config()

    logger.info("Building RAG chain")

    vector_store = build_or_load_vector_store(transcript, chroma_path)

    retriever = vector_store.as_retriever(
        search_type=config.rag_search_type,
        search_kwargs={
            "k": config.rag_retriever_k,
            "fetch_k": config.rag_retriever_fetch_k,
        },
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    def retrieve(query: str) -> str:
        docs = retriever.invoke(query)
        return format_docs(docs)

    rag_chain = (
        {
            "context": RunnableLambda(retrieve),
            "question": RunnablePassthrough(),
        }
        | prompt
        | get_llm()
        | StrOutputParser()
    )

    logger.info("RAG chain ready")
    return rag_chain


def ask_question(rag_chain, question: str) -> str:
    """
    Ask a question using the RAG chain.

    Args:
        rag_chain: RAG chain from create_rag_chain.
        question: User question.

    Returns:
        Answer from LLM.
    """
    logger.debug(f"Question: {question}")
    return rag_chain.invoke(question)