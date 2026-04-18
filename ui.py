import html
import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 2.4rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top, #081122 0%, #050b17 45%, #030814 100%);
    }

    .app-header {
        padding: 0.6rem 0 1.2rem 0;
    }

    .app-title {
        font-size: 2.45rem;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 0.35rem;
        color: #f5f7fb;
        letter-spacing: -0.02em;
    }

    .app-subtitle {
        font-size: 1rem;
        color: #98a6b8;
        margin-bottom: 0.2rem;
    }

    .metric-card {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(18,24,39,0.95), rgba(11,16,28,0.94));
        border: 1px solid rgba(130, 151, 192, 0.14);
        box-shadow: 0 8px 28px rgba(0,0,0,0.18);
        min-height: 105px;
    }

    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #a9b4c4;
        margin-bottom: 0.45rem;
    }

    .metric-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f7f9fc;
        line-height: 1.35;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(28,31,44,0.96), rgba(25,28,39,0.96));
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    .sidebar-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 0.35rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 52px;
        border-radius: 14px 14px 0 0;
        padding: 0 1.25rem;
        background: transparent;
        color: #b4bfd1;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #7c4dff !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 14px !important;
        min-height: 48px !important;
        border: 1px solid rgba(124, 77, 255, 0.35) !important;
        background: linear-gradient(180deg, rgba(14,20,35,0.96), rgba(9,14,26,0.96)) !important;
        color: #f4f6fb !important;
        font-weight: 600 !important;
        transition: 0.2s ease;
    }

    .stTextArea textarea,
    .stTextInput input,
    [data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {
        border-radius: 14px !important;
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        color: #f5f7fb !important;
    }

    .chat-row {
        display: flex;
        width: 100%;
        margin: 0.9rem 0 1.2rem 0;
    }

    .chat-row.user {
        justify-content: flex-end;
    }

    .chat-row.assistant {
        justify-content: flex-start;
    }

    .chat-bubble {
        max-width: 78%;
        padding: 1rem 1.15rem;
        border-radius: 22px;
        position: relative;
        box-shadow: 0 12px 30px rgba(0,0,0,0.16);
        border: 1px solid rgba(255,255,255,0.07);
    }

    .chat-bubble.user {
        background: linear-gradient(135deg, rgba(24,108,255,0.95), rgba(32,120,255,0.88));
        color: #ffffff;
        border-top-right-radius: 10px;
        border: 1px solid rgba(110,170,255,0.28);
    }

    .chat-bubble.assistant {
        background: linear-gradient(180deg, rgba(21,28,47,0.97), rgba(11,17,31,0.97));
        color: #f4f7fb;
        border-top-left-radius: 10px;
        border: 1px solid rgba(155,95,255,0.25);
        box-shadow: inset 0 0 0 1px rgba(124,77,255,0.08), 0 12px 30px rgba(0,0,0,0.16);
    }

    .chat-meta {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.65rem;
        font-size: 0.88rem;
        font-weight: 700;
        color: #dbe4f0;
    }

    .chat-avatar {
        width: 34px;
        height: 34px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }

    .chat-avatar.user {
        background: rgba(255,255,255,0.18);
    }

    .chat-avatar.assistant {
        background: linear-gradient(135deg, rgba(255,74,156,0.9), rgba(120,68,255,0.85));
    }

    .chat-content {
        font-size: 1.05rem;
        line-height: 1.8;
        word-wrap: break-word;
    }

    .quick-panel {
        padding: 1rem 1rem 0.7rem 1rem;
        border-radius: 18px;
        background: linear-gradient(180deg, rgba(18,24,39,0.95), rgba(11,16,28,0.94));
        border: 1px solid rgba(130, 151, 192, 0.14);
        box-shadow: 0 8px 28px rgba(0,0,0,0.18);
    }

    .quick-panel-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #f5f7fb;
        margin-bottom: 0.8rem;
    }

    .soft-divider {
        height: 1px;
        background: linear-gradient(90deg, rgba(255,255,255,0.03), rgba(255,255,255,0.12), rgba(255,255,255,0.03));
        margin: 1rem 0 1rem 0;
    }

    .small-note {
        color: #98a6b8;
        font-size: 0.92rem;
    }
    </style>
    """, unsafe_allow_html=True)


def model_display_name(model_name: str) -> str:
    mapping = {
        "Tharusha_Dilhara_Jayadeera/singemma": "SinGemma",
        "Tharusha_Dilhara_Jayadeera/singemma:latest": "SinGemma",
        "llama3:latest": "Llama 3",
        "gemma3:4b": "Gemma 3 4B",
    }
    return mapping.get(model_name, model_name.split("/")[-1])


def render_header():
    st.markdown(
        """
        <div class="app-header">
            <div class="app-title">💬 සිංහල Offline Chatbot</div>
            <div class="app-subtitle">Local OLLAMA models භාවිතයෙන් ක්‍රියාත්මක වන Sinhala chatbot application</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metric_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_chat_bubble(role: str, content: str):
    is_user = role == "user"
    bubble_class = "user" if is_user else "assistant"
    icon = "👤" if is_user else "🤖"
    title = "ඔබ" if is_user else "සහායකයා"
    safe_content = html.escape(content).replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="chat-row {bubble_class}">
            <div class="chat-bubble {bubble_class}">
                <div class="chat-meta">
                    <span class="chat-avatar {bubble_class}">{icon}</span>
                    <span>{title}</span>
                </div>
                <div class="chat-content">{safe_content}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )