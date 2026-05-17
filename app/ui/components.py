"""Reusable UI components for the Streamlit application."""

import html

import streamlit as st


def step_status(steps: dict, key: str) -> str:
    """Get CSS class for pipeline step status."""
    s = steps.get(key, "pending")
    if s == "active":
        return "dot-active"
    if s == "done":
        return "dot-done"
    return "dot-pending"


def render_step_bar(label: str, key: str, icon: str) -> None:
    """
    Render a pipeline step status bar.

    Args:
        label: Display label for the step.
        key: Session state key for this step.
        icon: Emoji icon for the step.
    """
    steps = st.session_state.get("pipeline_steps", {})
    css = step_status(steps, key)
    step_label = f"{icon} {label}".strip() if icon else label
    st.markdown(
        f"""
        <div class="status-bar">
            <div class="status-dot {css}"></div>
            <span>{step_label}</span>
        </div>""",
        unsafe_allow_html=True,
    )


def render_pipeline_train() -> None:
    """Render the main workflow as a horizontal train."""
    steps = st.session_state.get("pipeline_steps", {})

    def node_class(key: str) -> str:
        state = steps.get(key, "pending")
        if state == "done":
            return "train-node-done"
        if state == "active":
            return "train-node-active"
        return "train-node-pending"

    def connector_class(key: str) -> str:
        return "train-connector-done" if steps.get(key) == "done" else "train-connector-pending"

    st.markdown(
        f"""
        <div class="train-shell">
            <div class="pipeline-tag">AI PIPELINE</div>
            <div class="train-copy">
                Extract clean audio, build searchable context, and ask follow-up questions without changing the original workflow.
            </div>
            <div class="train-track">
                <div class="train-locomotive train-node-pending">🚂</div>
                <div class="train-connector {connector_class('audio')}"></div>
                <div class="train-stop">
                    <div class="train-node {node_class('audio')}"></div>
                    <div class="train-stop-copy">
                        <div class="train-stop-title">Audio Extraction</div>
                        <div class="train-stop-subtitle">Extract clean audio</div>
                    </div>
                </div>
                <div class="train-connector {connector_class('summary')}"></div>
                <div class="train-stop">
                    <div class="train-node {node_class('summary')}"></div>
                    <div class="train-stop-copy">
                        <div class="train-stop-title">Transcript + Summary</div>
                        <div class="train-stop-subtitle">Build searchable context</div>
                    </div>
                </div>
                <div class="train-connector {connector_class('rag')}"></div>
                <div class="train-stop">
                    <div class="train-node {node_class('rag')}"></div>
                    <div class="train-stop-copy">
                        <div class="train-stop-title">RAG Chat</div>
                        <div class="train-stop-subtitle">Ask follow-up questions</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    """Render the empty state when no video is processed."""
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">🎬</div>
        <div class="section-header empty-state-title">
            Ready to analyze
        </div>
        <div class="section-subtitle empty-state-copy">
            Paste a YouTube link or upload a local file in the sidebar, choose a language, and click <strong>Analyze</strong> to start.
        </div>
        <div class="empty-state-badges">
            <span class="badge badge-purple">Transcription</span>
            <span class="badge badge-cyan">Summarization</span>
            <span class="badge badge-green">RAG Chat</span>
        </div>
    </div>""", unsafe_allow_html=True)


def render_chat_history() -> None:
    """Render chat history from session state."""
    if not st.session_state.get("chat_history"):
        st.markdown("""
        <div class="card chat-empty-state">
            <div class="chat-empty-icon">🤖</div>
            <div class="section-subtitle">Ask anything about the transcript. The assistant will answer from the processed video or meeting context.</div>
        </div>""", unsafe_allow_html=True)
        return

    chat_html = '<div class="chat-container">'
    for msg in st.session_state.chat_history:
        content = html.escape(msg['content']).replace('\n', '<br>')
        if msg["role"] == "user":
            chat_html += f"""
            <div class="chat-msg chat-msg-user">
                <span class="chat-label user-label">You</span>
                <div class="chat-bubble user-bubble">{content}</div>
            </div>"""
        else:
            chat_html += f"""
            <div class="chat-msg chat-msg-assistant">
                <span class="chat-label bot-label">🤖 Assistant</span>
                <div class="chat-bubble bot-bubble">{content}</div>
            </div>"""
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
