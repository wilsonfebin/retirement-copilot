# =============================================================================
# app/main.py
# =============================================================================

import time
import streamlit as st

from app.ui.charts import (
    render_corpus_growth_chart
)

from app.ui.styles import load_css

from app.guardrails.retrieval_guard import (
    validate_retrieval
)

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

from app.agents.orchestrator import (
    detect_filters,
    build_context,
    extract_recommended_plans,
    stream_response
)

from app.rag.retriever import (
    retrieve_documents
)

from app.agents.simulation_agent import (
    run_retirement_simulation
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
    run_retirement_simulation(

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

    # =========================================================================
    # ACTIVE CONVERSATION
    # =========================================================================

    current_conversation = (

        st.session_state.conversations[
            st.session_state.active_conversation
        ]
    )

    # =========================================================================
    # FOLLOW-UP DETECTION
    # =========================================================================

    is_follow_up = (

        len(
            current_conversation["messages"]
        ) > 0
    )

    # =========================================================================
    # LIGHTWEIGHT CONVERSATION MEMORY
    # =========================================================================

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

    # =========================================================================
    # QUERY BUILDING
    # =========================================================================

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

    # =========================================================================
    # FINANCIAL TARGET EXTRACTION
    # =========================================================================

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

    # =========================================================================
    # FILTERS
    # =========================================================================

    filters = detect_filters(
        query
    )

    # =========================================================================
    # QUERY VALIDATION
    # =========================================================================

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
    # STATUS
    # =========================================================================

    workflow_container = st.container()

    response_placeholder = st.empty()

    streamed_text = ""

    backend_time = 0

    prompt_tokens = 0

    completion_tokens = 0

    total_tokens = 0

    estimated_cost = 0

    with workflow_container:

        with st.status(

            "Processing retirement analysis...",

            expanded=True

        ) as status:

            # ================================================================
            # RETRIEVAL
            # ================================================================

            st.write(
                "🔍 Retrieving pension documents..."
            )

            documents = retrieve_documents(

                query=query,

                filters=filters,

                k=4
            )

            guardrail_result = (
                validate_retrieval(
                    documents
                )
            )

            if not guardrail_result["is_valid"]:

                st.error(
                    guardrail_result["reason"]
                )

                st.stop()

            retrieval_context = (
                build_context(
                    documents
                )
            )

            recommended_plans = (
                extract_recommended_plans(
                    documents
                )
            )

            # ================================================================
            # SIMULATION
            # ================================================================

            st.write(
                "📈 Running retirement simulations..."
            )

            simulation_result = (
                run_retirement_simulation(

                    current_age=current_age,

                    retirement_age=retirement_age,

                    current_corpus=current_corpus,

                    monthly_investment=monthly_investment,

                    annual_return=annual_return
                )
            )

            # ================================================================
            # GENERATION
            # ================================================================

            st.write(
                "🤖 Generating retirement insights..."
            )

            status.update(

                label="Streaming response...",

                state="running"
            )

            # ================================================================
            # STREAM RESPONSE
            # ================================================================

            for event in stream_response(

                query=query,

                retrieval_context=retrieval_context,

                simulation_result=simulation_result,

                conversation_history=conversation_history
            ):

                if event["type"] == "content":

                    streamed_text = (
                        event["full_response"]
                    )

                    response_placeholder.markdown(

                        f"""
<div class="assistant-card">

{streamed_text}▌

</div>
""",

                        unsafe_allow_html=True
                    )

                elif event["type"] == "complete":

                    backend_time = (
                        event["backend_time"]
                    )

                    prompt_tokens = (
                        event["prompt_tokens"]
                    )

                    completion_tokens = (
                        event["completion_tokens"]
                    )

                    total_tokens = (
                        event["total_tokens"]
                    )

                    estimated_cost = (
                        event["estimated_cost"]
                    )

            status.update(

                label="Analysis complete",

                state="complete"
            )

    frontend_end = time.time()

    frontend_time = round(

        frontend_end - frontend_start,

        2
    )

    # =========================================================================
    # FINAL STRUCTURED RESPONSE
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
    # UNIQUE SOURCES
    # =========================================================================

    unique_sources = {}

    for doc in documents:

        source = doc.metadata.get(

            "source",

            "Unknown"
        )

        if source not in unique_sources:

            unique_sources[source] = {

                "source": source,

                "content":
                    doc.page_content[:1500]
            }

    formatted_documents = list(
        unique_sources.values()
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
    # APPEND MESSAGE
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

    # =========================================================================
    # CLEAN STREAM PLACEHOLDER
    # =========================================================================

    response_placeholder.empty()


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