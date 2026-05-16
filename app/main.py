"""Streamlit web application for AI Video Assistant."""

from __future__ import annotations

import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from app.ui.components import (
    render_chat_history,
    render_empty_state,
    render_pipeline_train,
    render_step_bar,
)
from app.ui.styles import get_custom_css

load_dotenv()

st.set_page_config(
    page_title="Video & Meeting AI Chat-Assistant",
    page_icon="V",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_custom_css(), unsafe_allow_html=True)


ALLOWED_UPLOAD_TYPES = ["mp4", "mkv", "mov", "avi", "webm", "m4v", "mp3", "wav", "m4a"]


def init_session_state() -> None:
    defaults: dict[str, Any] = {
        "result": None,
        "chat_history": [],
        "chat_prompt": "",
        "processing": False,
        "pipeline_done": False,
        "pipeline_steps": {},
        "source_mode": "URL",
        "pipeline_source": None,
        "pipeline_language": "english",
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def reset_pipeline_state() -> None:
    st.session_state.result = None
    st.session_state.chat_history = []
    st.session_state.pipeline_steps = {}
    st.session_state.pipeline_done = False


def run_pipeline(source: str, language: str) -> None:
    from src.audio import process_input
    from src.processing import (
        extract_action_items,
        extract_key_decisions,
        extract_questions,
        generate_title,
        summarize,
    )
    from src.storage import ensure_cache_dir, generate_source_id, load_transcript, save_transcript
    from src.storage.vector import create_rag_chain
    from src.transcription import transcribe_all

    st.session_state.processing = True
    st.session_state.pipeline_steps = {"audio": "active"}

    try:
        source_id = generate_source_id(source)
        paths = ensure_cache_dir(source_id)

        transcript = load_transcript(paths.transcript)

        if transcript is None:
            chunks = process_input(source)
            st.session_state.pipeline_steps["audio"] = "done"
            st.session_state.pipeline_steps["transcript"] = "active"

            transcript = transcribe_all(chunks, language)
            save_transcript(transcript, paths.transcript)
            st.session_state.pipeline_steps["transcript"] = "done"
        else:
            st.session_state.pipeline_steps["audio"] = "done"
            st.session_state.pipeline_steps["transcript"] = "done"

        st.session_state.pipeline_steps["title"] = "active"
        title = generate_title(transcript)
        st.session_state.pipeline_steps["title"] = "done"

        st.session_state.pipeline_steps["summary"] = "active"
        summary = summarize(transcript)
        st.session_state.pipeline_steps["summary"] = "done"

        st.session_state.pipeline_steps["extract"] = "active"
        action_items = extract_action_items(transcript)
        decisions = extract_key_decisions(transcript)
        questions = extract_questions(transcript)
        st.session_state.pipeline_steps["extract"] = "done"

        st.session_state.pipeline_steps["rag"] = "active"
        rag_chain = create_rag_chain(transcript, paths.chroma)
        st.session_state.pipeline_steps["rag"] = "done"

        st.session_state.result = {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions,
            "rag_chain": rag_chain,
        }
        st.session_state.pipeline_done = True
        st.session_state.processing = False
        st.rerun()

    except Exception as exc:
        for key in ["audio", "transcript", "title", "summary", "extract", "rag"]:
            if st.session_state.pipeline_steps.get(key) == "active":
                st.session_state.pipeline_steps[key] = "pending"
        st.session_state.processing = False
        st.error(f"Error: {exc}")


def render_sidebar() -> tuple[str, str | None, Any, str, bool]:
    with st.sidebar:
        st.markdown(
            """
            <div class="hero-shell">
                <div class="hero-title" style="font-size:1.4rem">Video & Meeting</div>
                <div class="hero-sub">AI Chat-Assistant</div>
                <div class="section-subtitle sidebar-note" style="margin-top:0.85rem; color:#ffffff; letter-spacing:0.06em; font-size:0.78rem; line-height:1.5">
                    Videos <span style="display:inline-block; width:1.1em;"></span><span style="color:#ffffff;">&bull;</span><span style="display:inline-block; width:1.1em;"></span>Meetings <span style="display:inline-block; width:1.1em;"></span><span style="color:#ffffff;">&bull;</span><span style="display:inline-block; width:1.1em;"></span> Search
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        is_processing = st.session_state.get("processing", False)

        st.markdown('<div class="sidebar-section-title">Source</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle sidebar-note">Choose where the media comes from, then run the same processing pipeline.</div>',
            unsafe_allow_html=True,
        )
        source_mode = st.radio(
            "Source type",
            ["URL", "FILE"],
            horizontal=True,
            disabled=is_processing,
            key="source_mode",
            label_visibility="collapsed",
        )

        source_value: str | None = None
        uploaded_file: Any = None

        if source_mode == "URL":
            st.caption("Paste a YouTube or meeting link.")
            source_value = st.text_input(
                "Video URL",
                placeholder="https://youtube.com/watch?v=...",
                disabled=is_processing,
                label_visibility="collapsed",
            ).strip()
        else:
            st.caption("Upload a local video or audio file. It will be copied into downloads before processing.")
            st.markdown(
                '<div class="upload-guidance-tag">FILE UPLOADER</div>',
                unsafe_allow_html=True,
            )
            uploaded_file = st.file_uploader(
                "Upload File",
                type=ALLOWED_UPLOAD_TYPES,
                disabled=is_processing,
                accept_multiple_files=False,
                label_visibility="collapsed",
            )
            st.markdown(
                '<div class="upload-click-hint">Click Here!</div>',
                unsafe_allow_html=True,
            )
            if uploaded_file is not None:
                source_value = uploaded_file.name
                from src.audio import uploaded_file_already_exists

                if uploaded_file_already_exists(uploaded_file):
                    st.info(
                        "This file is already uploaded, so please click inside the File Uploader Box and upload the new file."
                    )
                else:
                    st.info(
                        "File selected. Click Analyse to process it. "
                        "If you want to replace it, use the FILE UPLOADER box above to choose another file."
                    )

        st.markdown('<div class="sidebar-section-title">Transcript</div>', unsafe_allow_html=True)
        language = st.selectbox(
            "Language",
            ["english", "hinglish"],
            index=0,
            disabled=is_processing,
        )

        if is_processing:
            st.markdown(
                """
                <style>
                    @keyframes spin-clockwise {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    @keyframes pulse-glow {
                        0%, 100% { box-shadow: 0 0 10px rgba(124, 58, 237, 0.5); }
                        50% { box-shadow: 0 0 25px rgba(124, 58, 237, 0.8), 0 0 40px rgba(6, 182, 212, 0.4); }
                    }
                    .processing-loader {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        padding: 1.5rem;
                        background: rgba(124, 58, 237, 0.08);
                        border: 1px solid rgba(124, 58, 237, 0.3);
                        border-radius: 12px;
                        margin-top: 0.5rem;
                    }
                    .spinner-ring {
                        width: 50px;
                        height: 50px;
                        border: 4px solid rgba(124, 58, 237, 0.2);
                        border-top: 4px solid #9f67ff;
                        border-right: 4px solid #06b6d4;
                        border-radius: 50%;
                        animation: spin-clockwise 1s linear infinite, pulse-glow 2s ease-in-out infinite;
                    }
                    .processing-text {
                        margin-top: 1rem;
                        font-family: 'Syne', sans-serif;
                        font-size: 0.85rem;
                        font-weight: 700;
                        color: #9f67ff;
                        letter-spacing: 0.05em;
                    }
                    .processing-subtext {
                        font-size: 0.7rem;
                        color: #8888aa;
                        margin-top: 0.3rem;
                    }
                </style>
                <div class="processing-loader">
                    <div class="spinner-ring"></div>
                    <div class="processing-text">ANALYSING VIDEO</div>
                    <div class="processing-subtext">Please wait...</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            run_btn = False
        else:
            run_btn = st.button("Analyse", use_container_width=True)

        if st.session_state.pipeline_done:
            st.markdown("---")
            st.markdown(
                '<div class="workflow-tag sidebar-workflow-tag">AI WORKFLOW</div>',
                unsafe_allow_html=True,
            )
            for step, icon, label in [
                ("audio", "A", "Audio Processing"),
                ("transcript", "T", "Transcription"),
                ("title", "N", "Title Generation"),
                ("summary", "S", "Summarisation"),
                ("extract", "E", "Extraction"),
                ("rag", "R", "RAG Engine"),
            ]:
                render_step_bar(label, step, icon)

    return source_mode, source_value, uploaded_file, language, run_btn


def render_main_area() -> None:
    st.markdown(
        """
        <div class="hero-shell">
            <div class="badge badge-cyan">Meeting intelligence workspace</div>
            <div class="hero-title hero-title-spaced">Video & Meeting AI Chat-Assistant</div>
            <div class="hero-sub">Transcribe | Summarise | Chat with your videos and meetings</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_pipeline_train()


def render_processing_overlay() -> None:
    if st.session_state.get("processing") and not st.session_state.get("pipeline_done"):
        st.markdown(
            """
            <div class="processing-shell">
                <style>
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                    @keyframes pulse-glow-main {
                        0%, 100% { box-shadow: 0 0 20px rgba(124, 58, 237, 0.4); }
                        50% { box-shadow: 0 0 40px rgba(124, 58, 237, 0.7), 0 0 60px rgba(6, 182, 212, 0.4); }
                    }
                </style>
                <div class="loader-ring"></div>
                <div class="processing-heading">Analysing Video</div>
                <div class="processing-subheading">Processing your video...</div>
                <div class="processing-progress">
                    <div class="processing-progress-fill"></div>
                </div>
                <div class="processing-steps">
                    <span>Extracting audio</span>
                    <span>Transcribing</span>
                    <span>Building RAG</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_results(result: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">Title</div>
            <div class="result-title">{result["title"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Summary</div>
                <div class="card-content">{result["summary"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Full Transcript</div>
                <div class="transcript-box">{result["transcript"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Action Items</div>
                <div class="card-content">{result["action_items"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Key Decisions</div>
                <div class="card-content">{result["key_decisions"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Open Questions</div>
                <div class="card-content">{result["open_questions"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")


def render_chat(result: dict[str, Any]) -> None:
    from src.storage.vector import ask_question

    st.markdown(
        '<div class="chat-arena-heading">Video & Meeting Chat Arena</div>',
        unsafe_allow_html=True,
    )

    render_chat_history()

    with st.form("chat_form", clear_on_submit=True):
        chat_col1, chat_col2 = st.columns([5, 1], gap="small")
        with chat_col1:
            user_input = st.text_input(
                "Ask a follow-up question",
                placeholder="Ask a follow-up question",
                label_visibility="collapsed",
                key="chat_prompt",
            )
        with chat_col2:
            send_btn = st.form_submit_button("Send", use_container_width=True)

    if send_btn and user_input.strip():
        with st.spinner("Thinking..."):
            answer = ask_question(result["rag_chain"], user_input.strip())
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown('<div id="chat-bottom"></div>', unsafe_allow_html=True)

    if st.session_state.chat_history:
        components.html(
            """
            <script>
                setTimeout(() => {
                    const target = window.parent.document.getElementById("chat-bottom");
                    if (target) {
                        target.scrollIntoView({behavior: "smooth", block: "end"});
                    } else {
                        window.parent.scrollTo({top: document.body.scrollHeight, behavior: "smooth"});
                    }
                }, 50);
            </script>
            """,
            height=0,
        )


def main() -> None:
    init_session_state()

    source_mode, source_value, uploaded_file, language, run_btn = render_sidebar()
    render_main_area()
    render_processing_overlay()

    if run_btn:
        if source_mode == "URL":
            if not source_value:
                st.error("Please enter a YouTube URL.")
            else:
                reset_pipeline_state()
                st.session_state.processing = True
                st.session_state.pipeline_source = source_value
                st.session_state.pipeline_language = language
                st.rerun()
        else:
            if uploaded_file is None:
                st.error("Please upload a local video or audio file.")
            else:
                from src.audio import save_uploaded_file

                try:
                    upload_result = save_uploaded_file(uploaded_file)
                except Exception as exc:
                    st.error(f"Unable to save uploaded file: {exc}")
                else:
                    if upload_result.already_exists:
                        st.info("This file has already been uploaded. Reusing the existing copy.")
                    else:
                        st.success("File uploaded successfully.")
                    reset_pipeline_state()
                    st.session_state.processing = True
                    st.session_state.pipeline_source = str(upload_result.path)
                    st.session_state.pipeline_language = language
                    st.rerun()

    if st.session_state.processing and not st.session_state.pipeline_done and st.session_state.get("pipeline_source"):
        run_pipeline(st.session_state.pipeline_source, st.session_state.pipeline_language)

    if st.session_state.result:
        render_results(st.session_state.result)
        render_chat(st.session_state.result)
    else:
        render_empty_state()


if __name__ == "__main__":
    main()
