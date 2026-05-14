# =============================================================================
# app/ui/styles.py
# =============================================================================

def load_css():

    return """
    <style>

    /* =========================================================================
       GLOBAL
    ========================================================================= */

    .stApp {

        background:
            linear-gradient(
                180deg,
                #020817 0%,
                #030b1d 100%
            );

        color: #FFFFFF;
    }

    .main .block-container {

        padding-top: 1.5rem;

        padding-bottom: 4rem;

        max-width: 96%;
    }

    h1, h2, h3, h4 {

        color: #FFFFFF;

        font-weight: 700;

        letter-spacing: -0.02em;
    }

    p, span, div {

        color: #E2E8F0;
    }

    hr {

        border-color:
            rgba(255,255,255,0.06);
    }

    /* =========================================================================
       SIDEBAR
    ========================================================================= */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #0b1220 0%,
                #0f172a 100%
            );

        border-right:
            1px solid rgba(255,255,255,0.05);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {

        color: white;
    }

    section[data-testid="stSidebar"] label {

        color: #CBD5E1 !important;

        font-weight: 500;
    }

    /* =========================================================================
       USER QUESTION CARD
    ========================================================================= */

    .user-question-card {

        background:
            linear-gradient(
                135deg,
                rgba(30,64,175,0.35),
                rgba(59,130,246,0.12)
            );

        border:
            1px solid rgba(96,165,250,0.22);

        border-radius: 18px;

        padding: 18px 22px;

        margin-top: 10px;

        margin-bottom: 14px;

        box-shadow:
            0 8px 30px rgba(0,0,0,0.28);
    }

    .user-question-text {

        color: white;

        font-size: 19px;

        font-weight: 600;

        line-height: 1.6;
    }

    /* =========================================================================
       AI RESPONSE CARD
    ========================================================================= */

    .assistant-card {

        background:
            linear-gradient(
                135deg,
                rgba(10,18,35,0.95),
                rgba(13,25,45,0.92)
            );

        border:
            1px solid rgba(255,255,255,0.06);

        border-radius: 22px;

        padding: 28px;

        margin-top: 12px;

        margin-bottom: 18px;

        box-shadow:
            0 12px 40px rgba(0,0,0,0.35);
    }

    .assistant-card h2 {

        margin-top: 10px;

        margin-bottom: 18px;

        font-size: 2rem;

        color: #FFFFFF;
    }

    .assistant-card ul {

        margin-top: 10px;

        margin-bottom: 18px;
    }

    .assistant-card li {

        margin-bottom: 12px;

        line-height: 1.7;
    }

    /* =========================================================================
       METRIC CARDS
    ========================================================================= */

    div[data-testid="metric-container"] {

        background:
            linear-gradient(
                135deg,
                #081325,
                #0b1830
            );

        border:
            1px solid rgba(255,255,255,0.06);

        padding: 22px;

        border-radius: 20px;

        min-height: 145px;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.30);
    }

    div[data-testid="metric-container"] label {

        color: #CBD5E1 !important;

        font-size: 15px;

        font-weight: 600;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {

        font-size: 3rem;

        font-weight: 700;

        color: white;
    }

    /* =========================================================================
       PLOTLY CHART CONTAINER
    ========================================================================= */

    .js-plotly-plot {

        border-radius: 22px;

        overflow: hidden;

        border:
            1px solid rgba(255,255,255,0.06);

        background:
            linear-gradient(
                135deg,
                #081325,
                #0b1830
            );

        padding: 8px;

        box-shadow:
            0 12px 35px rgba(0,0,0,0.35);
    }

    /* =========================================================================
       RECOMMENDED PLAN CARDS
    ========================================================================= */

    .plan-card {

        background:
            linear-gradient(
                135deg,
                #0d2a20,
                #123927
            );

        border-radius: 18px;

        padding: 18px 22px;

        border:
            1px solid rgba(255,255,255,0.05);

        margin-bottom: 14px;

        box-shadow:
            0 8px 24px rgba(0,0,0,0.24);
    }

    .plan-title {

        color: white;

        font-size: 20px;

        font-weight: 700;
    }

    /* =========================================================================
       SOURCE EXPANDERS
    ========================================================================= */

    .streamlit-expanderHeader {

        background:
            rgba(255,255,255,0.02);

        border-radius: 14px;

        border:
            1px solid rgba(255,255,255,0.04);
    }

    /* =========================================================================
       CHAT HISTORY BUTTONS
    ========================================================================= */

    .stButton > button {

        border-radius: 14px;

        min-height: 50px;

        font-weight: 600;

        border:
            1px solid rgba(255,255,255,0.06);

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.04),
                rgba(255,255,255,0.02)
            );

        color: white;

        transition:
            all 0.25s ease;
    }

    .stButton > button:hover {

        border:
            1px solid rgba(96,165,250,0.35);

        transform:
            translateY(-1px);

        box-shadow:
            0 10px 20px rgba(0,0,0,0.28);
    }

    /* =========================================================================
       CHAT INPUT
    ========================================================================= */

    .stChatInputContainer {

        border-top:
            1px solid rgba(255,255,255,0.05);

        background:
            rgba(2,8,23,0.98);

        backdrop-filter:
            blur(12px);
    }


    /* =========================================================================
       FOOTER METRICS
    ========================================================================= */

    .footer-metrics {

        opacity: 0.78;

        font-size: 13px;

        margin-top: 20px;

        margin-bottom: 10px;

        color: #94A3B8;
    }

    /* =========================================================================
       SUGGESTION BUTTONS
    ========================================================================= */

    .suggestion-button {

        margin-bottom: 12px;
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

    /* =========================================================================
       STREAMLIT INPUTS
    ========================================================================= */

    div[data-baseweb="input"] {

        background:
            rgba(255,255,255,0.03);

        border-radius: 14px;
    }

    div[data-baseweb="select"] > div {

        background:
            rgba(255,255,255,0.03) !important;

        border:
            1px solid rgba(255,255,255,0.05) !important;

        border-radius: 14px !important;
    }

    /* =========================================================================
       STATUS CONTAINER
    ========================================================================= */

    div[data-testid="stStatusWidget"] {

        background:
            rgba(255,255,255,0.03);

        border-radius: 16px;

        border:
            1px solid rgba(255,255,255,0.06);
    }

    </style>
    """