"""Custom CSS styles for the Streamlit application."""

# Keep all existing styles but organized in a function
STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --surface-2: #1a1a25;
    --border: #2a2a3a;
    --accent: #7c3aed;
    --accent-glow: #9f67ff;
    --accent-2: #06b6d4;
    --text: #e8e8f0;
    --text-muted: #8888aa;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
}

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg) !important;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(124, 58, 237, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(124, 58, 237, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: clamp(1.7rem, 3.8vw, 2.6rem);
    font-weight: 900;
    line-height: 1.1;
    margin: 0;
    letter-spacing: 0.05em;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 50%, var(--accent-2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.hero-title-spaced {
    margin-top: 0.8rem;
}

.sidebar-section-title {
    margin-top: 0.75rem;
    color: #f2c94c;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    text-decoration: underline;
    text-decoration-color: rgba(255,255,255,0.92);
    text-decoration-thickness: 1px;
    text-underline-offset: 4px;
    font-weight: 700;
}

.section-subtitle.sidebar-note {
    margin-bottom: 0.6rem;
    font-size: 0.72rem !important;
    color: var(--text-muted) !important;
    line-height: 1.55 !important;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] {
    background: linear-gradient(180deg, rgba(17, 17, 24, 0.96), rgba(26, 26, 37, 0.96));
    border: 1px solid rgba(42, 42, 58, 0.95);
    border-radius: 14px;
    padding: 0.65rem 0.75rem 0.5rem;
    margin: 0.2rem 0 0.75rem;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
    gap: 0.4rem;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    background: rgba(10, 10, 15, 0.65);
    border: 1px solid rgba(42, 42, 58, 0.9);
    border-radius: 999px;
    padding: 0.32rem 0.7rem;
    min-height: 0;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.28), rgba(6,182,212,0.16));
    border-color: rgba(124,58,237,0.45);
}

[data-testid="stSidebar"] div[data-testid="stFileUploader"] {
    background: linear-gradient(180deg, rgba(17, 17, 24, 0.96), rgba(26, 26, 37, 0.96));
    border: 1px solid rgba(42, 42, 58, 0.95);
    border-radius: 14px;
    padding: 0.65rem 0.75rem 0.75rem;
    margin-top: 0.15rem;
}

[data-testid="stSidebar"] div[data-testid="stTextInput"] {
    margin-bottom: 0.55rem;
}

[data-testid="stSidebar"] div[data-testid="stFileUploaderDropzone"] {
    background: rgba(10, 10, 15, 0.55) !important;
    border: 1px dashed rgba(124, 58, 237, 0.45) !important;
    border-radius: 12px !important;
    padding: 0.55rem !important;
}

[data-testid="stSidebar"] div[data-testid="stFileUploaderDropzone"] * {
    color: var(--text) !important;
}

[data-testid="stSidebar"] div[data-testid="stFileUploaderDropzone"] button {
    border-radius: 999px !important;
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
}

.upload-guidance-tag {
    display: inline-flex;
    align-items: center;
    margin: 0.15rem 0 0.45rem;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    background: rgba(124, 58, 237, 0.16);
    border: 1px solid rgba(124, 58, 237, 0.3);
    color: var(--accent-glow) !important;
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.workflow-tag {
    display: inline-flex;
    align-items: center;
    margin: 0 0 0.75rem;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    background: rgba(124, 58, 237, 0.16);
    border: 1px solid rgba(124, 58, 237, 0.3);
    color: var(--accent-glow) !important;
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.sidebar-workflow-tag {
    margin: 0.65rem 0 0.75rem;
}

.pipeline-tag {
    display: inline-flex;
    align-items: center;
    margin: 0 0 0.85rem;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    background: rgba(6, 182, 212, 0.14);
    border: 1px solid rgba(6, 182, 212, 0.32);
    color: var(--accent-2) !important;
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.upload-click-hint {
    position: relative;
    margin-top: -5.2rem;
    margin-left: 0.95rem;
    width: fit-content;
    padding: 0.3rem 0.7rem;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.88);
    color: #111118 !important;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.18);
    pointer-events: none;
}

[data-testid="stSidebar"] button[kind="secondary"] {
    background: var(--surface-2) !important;
}

[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
    color: white !important;
}

[data-testid="stSidebar"] div[data-testid="stAlert"] {
    font-size: 0.78rem !important;
    line-height: 1.45 !important;
}

[data-testid="stSidebar"] div[data-testid="stAlert"] p {
    font-size: 0.78rem !important;
    line-height: 1.45 !important;
    letter-spacing: 0.08em !important;
}

.section-subtitle.sidebar-note {
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    line-height: 1.5 !important;
    color: #ffffff !important;
}

.train-shell {
    margin-top: 1rem;
    margin-bottom: 1.25rem;
    padding: 1.05rem 1.2rem 1rem;
    background: linear-gradient(180deg, rgba(17, 17, 24, 0.92), rgba(12, 15, 24, 0.96));
    border: 1px solid var(--border);
    border-radius: 20px;
    box-shadow: var(--shadow);
}

.train-copy {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text-muted);
    font-size: 0.92rem;
    line-height: 1.55;
    margin-bottom: 1rem;
}

.train-track {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    overflow-x: auto;
    padding-bottom: 0.25rem;
}

.train-locomotive {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex: 0 0 auto;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.train-stop {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    min-width: 176px;
    flex: 0 0 auto;
}

.train-node {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    flex: 0 0 auto;
    border: 2px solid rgba(255, 255, 255, 0.06);
}

.train-node-pending {
    background: #5f6579;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.06);
}

.train-node-active {
    background: var(--accent-glow);
    box-shadow: 0 0 0 5px rgba(159, 103, 255, 0.12), 0 0 14px rgba(159, 103, 255, 0.65);
    animation: pulse 1.4s infinite;
}

.train-node-done {
    background: var(--success);
    box-shadow: 0 0 0 5px rgba(16, 185, 129, 0.12), 0 0 14px rgba(16, 185, 129, 0.5);
}

.train-stop-copy {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.train-stop-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text);
    white-space: nowrap;
}

.train-stop-subtitle {
    font-size: 0.65rem;
    color: var(--text-muted);
    line-height: 1.4;
}

.train-connector {
    flex: 0 0 64px;
    height: 2px;
    border-radius: 999px;
}

.train-connector-pending {
    background: linear-gradient(90deg, rgba(95, 101, 121, 0.55), rgba(95, 101, 121, 0.15));
}

.train-connector-done {
    background: linear-gradient(90deg, rgba(16,185,129,0.95), rgba(16,185,129,0.15));
}

.train-track::-webkit-scrollbar {
    height: 4px;
}

.train-track::-webkit-scrollbar-thumb {
    background: rgba(124, 58, 237, 0.25);
}

.hero-metrics {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 1.25rem;
}

.metric-card {
    background: rgba(8, 12, 22, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    backdrop-filter: blur(10px);
}

.metric-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--text-muted);
}

.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text);
    margin-top: 0.35rem;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}

.card:hover {
    border-color: var(--accent);
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5rem 2rem;
    text-align: center;
}

.empty-state-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.empty-state-title {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.empty-state-copy {
    max-width: 420px;
}

.empty-state-badges {
    margin-top: 2rem;
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
}

.chat-empty-state {
    text-align: center;
    padding: 2rem;
}

.chat-empty-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 8px rgba(124,58,237,0.5));
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.card-content {
    font-size: 0.875rem;
    line-height: 1.7;
    color: var(--text);
}

.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.badge-purple { background: rgba(124,58,237,0.2); color: var(--accent-glow); border: 1px solid rgba(124,58,237,0.3); }
.badge-cyan   { background: rgba(6,182,212,0.15); color: var(--accent-2);    border: 1px solid rgba(6,182,212,0.3); }
.badge-green  { background: rgba(16,185,129,0.15); color: var(--success);    border: 1px solid rgba(16,185,129,0.3); }
.badge-workflow {
    background: rgba(6,182,212,0.10);
    color: #33d8f3;
    border: 1px solid rgba(6,182,212,0.38);
    padding: 0.16rem 0.48rem;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.14em;
}

.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}

.stButton > button[kind="secondary"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
}

div[data-testid="stBottomBlockContainer"],
div[data-testid="stBottomBlockContainer"] > div,
div[data-testid="stChatInput"] {
    background: linear-gradient(180deg, rgba(17, 17, 24, 0.98), rgba(12, 15, 24, 0.98)) !important;
    border-top: 1px solid var(--border) !important;
    padding: 0.85rem 1rem 1rem !important;
}

div[data-testid="stBottomBlockContainer"] * {
    background-color: transparent !important;
}

div[data-testid="stChatInput"] {
    background: linear-gradient(180deg, rgba(17, 17, 24, 0.98), rgba(12, 15, 24, 0.98)) !important;
}

div[data-testid="stChatInput"] > div {
    background: transparent !important;
}

div[data-testid="stChatInput"] textarea,
div[data-testid="stChatInput"] div[data-baseweb="base-input"],
div[data-testid="stChatInput"] div[data-baseweb="textarea"] {
    background: var(--surface-2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

div[data-testid="stChatInput"] textarea::placeholder,
div[data-testid="stChatInput"] input::placeholder {
    color: var(--text-muted) !important;
}

div[data-testid="stChatInput"] button,
div[data-testid="stBottomBlockContainer"] button {
    background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
    color: white !important;
    border: none !important;
}

div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.68rem 1rem !important;
    text-transform: uppercase !important;
    min-height: 48px !important;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}

.status-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem 0.75rem 1.25rem;
    background: var(--surface);
    border-radius: 8px;
    margin: 0.4rem 0;
    border: 1px solid var(--border);
    font-size: 0.8rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}

.status-bar:hover {
    border-color: var(--accent);
}

.status-bar::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
}

.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.dot-active   { background: var(--accent-glow); box-shadow: 0 0 8px var(--accent-glow); animation: pulse 1.5s infinite; }
.dot-done     { background: var(--success); }
.dot-pending  { background: var(--border); }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

.chat-container {
    background: var(--surface) !important;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    max-height: 420px;
    overflow-y: auto;
    margin-bottom: 1rem;
}

.chat-msg {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.chat-msg-user {
    align-items: flex-end;
}

.chat-msg-assistant {
    align-items: flex-start;
}

.chat-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.chat-bubble {
    display: inline-block;
    padding: 0.6rem 1rem;
    border-radius: 10px;
    font-size: 0.875rem;
    line-height: 1.6;
    max-width: 90%;
    color: var(--text) !important;
}

.user-label  { color: var(--accent-glow) !important; }
.bot-label   { color: var(--accent-2) !important; }

.user-bubble { background: rgba(124,58,237,0.25) !important; border: 1px solid rgba(124,58,237,0.4) !important; align-self: flex-end; color: var(--text) !important; }
.bot-bubble  { background: rgba(6,182,212,0.15) !important;  border: 1px solid rgba(6,182,212,0.3) !important;   align-self: flex-start; color: var(--text) !important; }

hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

.transcript-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem;
    font-size: 0.82rem;
    line-height: 1.8;
    max-height: 300px;
    overflow-y: auto;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}

div[data-testid="stExpanderContent"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

div[data-testid="stExpanderContent"] .transcript-box {
    background: var(--surface-2) !important;
    color: #b8b8d0 !important;
}

.stExpander {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

.stExpander::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
    border-radius: 12px 0 0 12px;
}

div[data-testid="stExpanderContent"] {
    border-top: 1px solid var(--border) !important;
    border-radius: 0 0 11px 11px !important;
}

.stProgress > div > div > div { background: var(--accent) !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label { color: var(--text-muted) !important; font-size: 0.8rem !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

[data-testid="stMarkdownContainer"] img { filter: none !important; opacity: 1 !important; }

.progress-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.progress-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.75rem;
}

.progress-track {
    height: 12px;
    background: var(--surface-2);
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border);
    margin-bottom: 1rem;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #ef4444 0%, #f59e0b 30%, #10b981 100%);
    border-radius: 6px;
    transition: width 0.5s ease-out;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}

.progress-steps {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
}

.step-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 600;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-muted);
    transition: all 0.3s ease;
}

.step-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    font-weight: 600;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--text-muted);
    transition: all 0.3s ease;
}

.step-audio.active   { background: rgba(239,68,68,0.3); border-color: #ef4444; color: #ef4444; }
.step-transcript.active { background: rgba(249,115,22,0.3); border-color: #f97316; color: #f97316; }
.step-title.active   { background: rgba(234,179,8,0.3); border-color: #eab308; color: #eab308; }
.step-summary.active { background: rgba(132,204,22,0.3); border-color: #84cc16; color: #84cc16; }
.step-extract.active { background: rgba(34,197,94,0.3); border-color: #22c55e; color: #22c55e; }
.step-rag.active     { background: rgba(16,185,129,0.3); border-color: #10b981; color: #10b981; }

.processing-shell {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    margin: 1rem 0;
    text-align: center;
}

.loader-ring {
    width: 80px;
    height: 80px;
    border: 5px solid var(--surface-2);
    border-top: 5px solid #9f67ff;
    border-right: 5px solid #06b6d4;
    border-radius: 50%;
    animation: spin 1s linear infinite, pulse-glow-main 2s ease-in-out infinite;
    margin: 0 auto 1.5rem;
}

.processing-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.5rem;
}

.processing-subheading {
    color: var(--accent-glow);
    font-size: 0.95rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

.processing-progress {
    background: var(--surface-2);
    height: 12px;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border);
}

.processing-progress-fill {
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, #7c3aed, #06b6d4, #8b5cf6, #06b6d4, #7c3aed);
    background-size: 300% 100%;
    border-radius: 6px;
    animation: progress-flow 2s linear infinite;
}

@keyframes progress-flow {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

.processing-steps {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 1.5rem;
    gap: 1rem;
    color: var(--text-muted);
    font-size: 0.8rem;
}

.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text);
}

.chat-arena-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #e8e8f0;
}


</style>
"""


def get_custom_css() -> str:
    """Return the custom CSS styles."""
    return STYLES
