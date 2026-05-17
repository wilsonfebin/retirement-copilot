# =============================================================================
# app/main.py
# =============================================================================

import time
import streamlit as st

from app.ui.charts import (
    render_corpus_growth_chart
)

from app.ui.styles import load_css

from app.guardrails.intent_guard import (
    classify_query_intent
)

from app.agents.query_parser import (
    extract_financial_targets
)

from app.ui.sidebar import (
    render_knowledge_modules,
    render_chat_history,
    render_chat_controls
)

from app.ui.chat import (
    render_user_message,
    render_assistant_message
)

from app.ui.cards import (
    render_projection_cards,
    render_recommended_plans,
    render_sources
)

from app.ui.metrics import (
    render_footer_metrics
)

from app.api.simulation_client import (
    get_retirement_simulation
)

from app.api.analysis_client import (
    stream_retirement_analysis
)

from app.utils.helpers import (
    format_retirement_response
)


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(

    page_title="Retirement CoPilot",

    page_icon="💰",

    layout="wide"
)


# =============================================================================
# LOAD CSS
# =============================================================================

st.markdown(

    load_css(),

    unsafe_allow_html=True
)


# =============================================================================
# SESSION STATE
# =============================================================================

if "conversations" not in st.session_state:

    st.session_state.conversations = []


if "active_conversation" not in st.session_state:

    st.session_state.active_conversation = None


# =============================================================================
# HEADER
# =============================================================================

st.title(
    "💰 Retirement CoPilot"
)

st.markdown(
    """
AI-powered Retirement Analytics Dashboard
for HDFC Bank pension products.
"""
)


# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.header(
    "Customer Profile"
)

current_age = st.sidebar.number_input(

    "Current Age",

    18,

    80,

    40
)

retirement_age = st.sidebar.number_input(

    "Retirement Age",

    40,

    80,

    60
)

current_corpus = st.sidebar.number_input(

    "Current Corpus (₹)",

    value=0,

    step=50000
)

monthly_investment = st.sidebar.number_input(

    "Monthly SIP (₹)",

    value=10000,

    step=5000
)

risk_profile = st.sidebar.selectbox(

    "Risk Profile",

    ["low", "moderate", "high"]
)


# =============================================================================
# RISK-BASED RETURNS
# =============================================================================

if risk_profile == "low":

    annual_return = 0.07

elif risk_profile == "moderate":

    annual_return = 0.10

else:

    annual_return = 0.13


# =============================================================================
# LIVE SIMULATION PREVIEW
# =============================================================================

simulation_preview = (
    get_retirement_simulation(

        current_age=current_age,

        retirement_age=retirement_age,

        current_corpus=current_corpus,

        monthly_investment=monthly_investment,

        annual_return=annual_return
    )
)

render_projection_cards(
    simulation_preview
)

st.divider()

render_corpus_growth_chart(

    simulation_result=simulation_preview,

    risk_profile=risk_profile,

    annual_return=annual_return,

    monthly_investment=monthly_investment,

    retirement_age=retirement_age,

    target_monthly_income=None
)

st.divider()


# =============================================================================
# SIDEBAR COMPONENTS
# =============================================================================

render_knowledge_modules()

render_chat_history()

render_chat_controls()


# =============================================================================
# SUGGESTED QUESTIONS
# =============================================================================

st.subheader(
    "💡 Suggested Questions"
)

suggested_questions = [

    "My retirement projections?",

    "Gap Analysis: Am I on track for my retirement goals?",

    "Which pension plans provide guaranteed income?",

    "Which pension plans offer lifelong income after retirement?",

    "Key benefits of HDFC pension products?",

    "What happens if I stop SIP contributions?"
]

selected_question = None

question_cols = st.columns(3)

for idx, question in enumerate(
    suggested_questions
):

    col = question_cols[idx % 3]

    with col:

        if st.button(

            question,

            key=f"suggestion_{idx}"
        ):

            selected_question = question


# =============================================================================
# CHAT INPUT
# =============================================================================

user_query = st.chat_input(
    "Ask Retirement CoPilot..."
)

if selected_question:

    user_query = selected_question


# =============================================================================
# CREATE CHAT
# =============================================================================

if (
    user_query
    and
    st.session_state.active_conversation
    is None
):

    st.session_state.conversations.append(

        {
            "title": "New Chat",

            "messages": []
        }
    )

    st.session_state.active_conversation = (

        len(
            st.session_state.conversations
        ) - 1
    )


# =============================================================================
# QUERY EXECUTION
# =============================================================================

if user_query:

    frontend_start = time.time()

    current_conversation = (

        st.session_state.conversations[
            st.session_state.active_conversation
        ]
    )

    is_follow_up = (

        len(
            current_conversation["messages"]
        ) > 0
    )

    recent_messages = (

        current_conversation[
            "messages"
        ][-3:]
    )

    conversation_history = ""

    for msg in recent_messages:

        conversation_history += f"""
User:
{msg['question']}

Assistant Summary:
Previous retirement guidance discussed.
"""

    query = f"""
Current User Question:
{user_query}

Customer Profile:
Current age: {current_age}
Retirement age: {retirement_age}
Current corpus: ₹{current_corpus}
Monthly SIP: ₹{monthly_investment}
Risk profile: {risk_profile}

Conversation Context:
{conversation_history}
"""

    financial_targets = (
        extract_financial_targets(
            user_query
        )
    )

    target_pension = financial_targets.get(
        "target_pension"
    )

    target_corpus = financial_targets.get(
        "target_corpus"
    )

    is_valid_query = (
        classify_query_intent(
            user_query
        )
    )

    if not is_valid_query:

        st.error(
            "Query appears unrelated to retirement planning or pension products."
        )

        st.stop()

    # =========================================================================
    # STREAMING RESPONSE
    # =========================================================================

    streamed_text = ""

    recommended_plans = []

    formatted_documents = []

    backend_time = 0

    prompt_tokens = 0

    completion_tokens = 0

    total_tokens = 0

    estimated_cost = 0

    status_placeholder = st.empty()

    response_container = st.empty()

    status_placeholder.info(
        "🤖 Generating retirement insights..."
    )

    for event in stream_retirement_analysis(

        query=query,

        current_age=current_age,

        retirement_age=retirement_age,

        current_corpus=current_corpus,

        monthly_investment=monthly_investment,

        risk_profile=risk_profile,

        annual_return=annual_return
    ):

        # =====================================================================
        # TOKEN STREAM
        # =====================================================================

        if event["type"] == "token":

            streamed_text += (
                event["content"]
            )

            response_container.text(

                streamed_text + "▌"
            )

        # =====================================================================
        # FINAL EVENT
        # =====================================================================

        elif event["type"] == "complete":

            recommended_plans = (
                event[
                    "recommended_plans"
                ]
            )

            formatted_documents = (
                event[
                    "documents"
                ]
            )

            backend_time = (
                event[
                    "backend_time"
                ]
            )

            prompt_tokens = (
                event[
                    "prompt_tokens"
                ]
            )

            completion_tokens = (
                event[
                    "completion_tokens"
                ]
            )

            total_tokens = (
                event[
                    "total_tokens"
                ]
            )

            estimated_cost = (
                event[
                    "estimated_cost"
                ]
            )

    status_placeholder.success(
        "✅ Analysis complete"
    )

    simulation_result = (
        simulation_preview
    )

    frontend_end = time.time()

    frontend_time = round(

        frontend_end - frontend_start,

        2
    )

    # =========================================================================
    # FORMAT RESPONSE
    # =========================================================================

    formatted_response = (

        format_retirement_response(

            simulation_result=
                simulation_result,

            recommended_plans=
                recommended_plans,

            generated_response=
                streamed_text,

            backend_time=
                backend_time,

            prompt_tokens=
                prompt_tokens,

            completion_tokens=
                completion_tokens,

            total_tokens=
                total_tokens,

            estimated_cost=
                estimated_cost
        )
    )

    # =========================================================================
    # UPDATE CHAT TITLE
    # =========================================================================

    if (

        current_conversation["title"]
        == "New Chat"
    ):

        current_conversation["title"] = (
            user_query[:40]
        )

    # =========================================================================
    # SAVE MESSAGE
    # =========================================================================

    current_conversation[
        "messages"
    ].append(

        {
            "question":
                user_query,

            "response":
                formatted_response,

            "documents":
                formatted_documents,

            "frontend_time":
                frontend_time,

            "is_follow_up":
                is_follow_up
        }
    )


# =============================================================================
# RENDER CONVERSATION HISTORY
# =============================================================================

if (

    len(st.session_state.conversations)
    > 0

    and

    st.session_state.active_conversation
    is not None
):

    conversation = (

        st.session_state.conversations[
            st.session_state.active_conversation
        ]
    )

    st.divider()

    st.subheader(
        "💬 Retirement Insights History"
    )

    reversed_messages = list(

        enumerate(
            conversation["messages"]
        )

    )[::-1]

    for idx, message in reversed_messages:

        render_user_message(
            message["question"]
        )

        render_assistant_message(

            message["response"][
                "generated_response"
            ]
        )

        render_recommended_plans(
            message["response"]
        )

        render_sources(
            message["documents"]
        )

        render_footer_metrics(

            message["response"],

            message["frontend_time"]
        )

        st.divider()