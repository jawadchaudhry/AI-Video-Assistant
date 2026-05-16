"""Command-line interface for AI Video Assistant."""

import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def validate_environment() -> None:
    """Validate required environment variables."""
    if not os.getenv("MISTRAL_API_KEY"):
        logger.error("MISTRAL_API_KEY is not set. Please set it in .env file.")
        sys.exit(1)


def warmup_models() -> None:
    """Warmup ML models before interactive use."""
    logger.info("Warming up Whisper model...")
    from src.transcription.whisper import load_model
    load_model()
    logger.info("Models ready")


def run_interactive() -> None:
    """Run in interactive mode for chat."""
    from src.audio import process_input
    from src.transcription import transcribe_all
    from src.processing import summarize, generate_title
    from src.processing import (
        extract_action_items,
        extract_key_decisions,
        extract_questions,
    )
    from src.storage import (
        generate_source_id,
        ensure_cache_dir,
        load_transcript,
        save_transcript,
    )
    from src.storage.vector import create_rag_chain, ask_question

    source = input("Enter YouTube URL or file path: ").strip()
    language = input("Language (english/hinglish): ").strip() or "english"

    logger.info(f"Processing: {source}")

    source_id = generate_source_id(source)
    paths = ensure_cache_dir(source_id)

    # Check for cached transcript
    transcript = load_transcript(paths.transcript)

    if transcript is None:
        logger.info("No cached transcript found, processing...")
        chunks = process_input(source)
        transcript = transcribe_all(chunks, language)
        save_transcript(transcript, paths.transcript)
    else:
        logger.info("Using cached transcript")

    # Generate outputs
    title = generate_title(transcript)
    summary = summarize(transcript)
    action_items = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    # Build RAG
    rag_chain = create_rag_chain(transcript, paths.chroma)

    # Print results
    print("\n" + "=" * 70)
    print(f"TITLE: {title}")
    print(f"\nSUMMARY:\n{summary}")
    print(f"\nACTION ITEMS:\n{action_items}")
    print(f"\nKEY DECISIONS:\n{decisions}")
    print(f"\nOPEN QUESTIONS:\n{questions}")
    print("=" * 70)

    # Interactive chat
    print("\nChat with your video (type 'exit' to quit)\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            break

        if not question:
            continue

        answer = ask_question(rag_chain, question)
        print(f"\nAI: {answer}\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Video Assistant - Meeting Intelligence System"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive chat mode",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate environment and exit",
    )

    args = parser.parse_args()

    if args.validate:
        validate_environment()
        logger.info("Environment validation passed")
        return

    validate_environment()

    if args.interactive:
        warmup_models()
        run_interactive()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()