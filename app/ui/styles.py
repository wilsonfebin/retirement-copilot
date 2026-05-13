def load_css():

    return """
    <style>

    /* =========================================================================
       GLOBAL
    ========================================================================= */

    .stApp {
        background-color: #020817;
        color: #FFFFFF;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 95%;
    }

    h1, h2, h3, h4 {
        color: #FFFFFF;
        font-weight: 700;
    }

    p, span, div {
        color: #E2E8F0;
    }

    hr {
        border-color: rgba(255,255,255,0.08);
    }

    /* =========================================================================
       SIDEBAR
    ========================================================================= */

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white;
    }

    /* =========================================================================
       USER QUESTION CARD
    ========================================================================= */

    .user-question-card {
        background: rgba(59,130,246,0.15);
        border: 1px solid rgba(59,130,246,0.35);
        border-radius: 14px;
        padding: 18px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .user-question-text {
        color: white;
        font-size: 18px;
        font-weight: 500;
        line-height: 1.6;
    }

    /* =========================================================================
       AI RESPONSE CARD
    ========================================================================= */

    .assistant-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
        margin-top: 12px;
        margin-bottom: 16px;
    }

    /* =========================================================================
       METRIC CARDS
    ========================================================================= */

    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 16px;
    }

    div[data-testid="metric-container"] label {
        color: #CBD5E1;
    }

    /* =========================================================================
       SOURCE EXPANDERS
    ========================================================================= */

    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
    }

    /* =========================================================================
       CHAT HISTORY BUTTONS
    ========================================================================= */

    .stButton > button {
        border-radius: 12px;
        min-height: 48px;
        font-weight: 500;
    }

    /* =========================================================================
       CHAT INPUT
    ========================================================================= */

    .stChatInputContainer {
        border-top: 1px solid rgba(255,255,255,0.08);
        background-color: #020817;
    }

    /* =========================================================================
       FOOTER METRICS
    ========================================================================= */

    .footer-metrics {
        opacity: 0.75;
        font-size: 13px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* =========================================================================
       SUGGESTION BUTTONS
    ========================================================================= */

    .suggestion-button {
        margin-bottom: 10px;
    }

    /* =========================================================================
       SCROLLBAR
    ========================================================================= */

    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #0F172A;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 20px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    </style>
    """
