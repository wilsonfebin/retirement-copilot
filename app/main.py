# =============================================================================
# app/main.py
# =============================================================================

import time
import streamlit as st

from app.ui.styles import load_css

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

from app.rag.retriever import retrieve_documents

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

st.title("💰 Retirement CoPilot")

st.markdown(
    """
AI-powered Retirement Planning CoPilot for HDFC Bank pension products.
"""
)


# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.header("Customer Profile")

current_age = st.sidebar.number_input(
    "Current Age",
    18,
    80,
    52
)

retirement_age = st.sidebar.number_input(
    "Retirement Age",
    40,
    80,
    60
)

current_corpus = st.sidebar.number_input(
    "Current Corpus (₹)",
    value=3500000,
    step=100000
)

monthly_investment = st.sidebar.number_input(
    "Monthly SIP (₹)",
    value=35000,
    step=5000
)

risk_profile = st.sidebar.selectbox(
    "Risk Profile",
    ["low", "moderate", "high"]
)


# =============================================================================
# SIDEBAR COMPONENTS
# =============================================================================

render_knowledge_modules()

render_chat_history()

render_chat_controls()


# =============================================================================
# SUGGESTED QUESTIONS
# =============================================================================

st.divider()

st.subheader("💡 Suggested Questions")

suggested_questions = [

    "Can I retire comfortably at 60?",

    "Why is my retirement readiness weak?",

    "How much SIP is needed for ₹1L pension?",

    "What pension can my corpus generate?",

    "Which plans provide guaranteed pension income?",

    "Market-linked or guaranteed plans?",

    "How much retirement corpus do I need?",

    "What happens if I stop SIP contributions?"
]

selected_question = None

question_cols = st.columns(4)

for idx, question in enumerate(
    suggested_questions
):

    col = question_cols[idx % 4]

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
    and st.session_state.active_conversation
    is None
):

    st.session_state.conversations.append(
        {
            "title": "New Chat",
            "messages": []
        }
    )

    st.session_state.active_conversation = (
        len(st.session_state.conversations) - 1
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
    # CONVERSATION MEMORY
    # =========================================================================

    recent_messages = current_conversation[
        "messages"
    ][-3:]

    conversation_history = ""

    for msg in recent_messages:

        conversation_history += f"""
User:
{msg['question']}

Assistant:
{msg['response']['generated_response'][:1200]}

"""

    # =========================================================================
    # QUERY BUILDING
    # =========================================================================

    if is_follow_up:

        query = f"""
        Previous conversation context:
        {conversation_history}

        Current question:
        {user_query}

        Customer profile:
        Current age: {current_age}
        Retirement age: {retirement_age}
        Current corpus: ₹{current_corpus}
        Monthly SIP: ₹{monthly_investment}
        Risk profile: {risk_profile}
        """

    else:

        query = f"""
        {user_query}

        Current age: {current_age}
        Retirement age: {retirement_age}
        Current corpus: ₹{current_corpus}
        Monthly SIP: ₹{monthly_investment}
        Risk profile: {risk_profile}
        """

    # =========================================================================
    # FILTERS
    # =========================================================================

    filters = detect_filters(query)

    # =========================================================================
    # LIVE STATUS + STREAMING
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

            retrieval_context = build_context(
                documents
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
                "📈 Running retirement simulation..."
            )

            simulation_result = (
                run_retirement_simulation(
                    current_age=current_age,
                    retirement_age=retirement_age,
                    current_corpus=current_corpus,
                    monthly_investment=monthly_investment,
                    annual_return=0.10
                )
            )

            # ================================================================
            # GENERATION
            # ================================================================

            st.write(
                "🤖 Thinking and generating response..."
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

                    streamed_text = event[
                        "full_response"
                    ]

                    response_placeholder.markdown(
                        f"""
<div class="assistant-card">
{streamed_text}▌
</div>
""",
                        unsafe_allow_html=True
                    )

                elif event["type"] == "complete":

                    backend_time = event[
                        "backend_time"
                    ]

                    prompt_tokens = event[
                        "prompt_tokens"
                    ]

                    completion_tokens = event[
                        "completion_tokens"
                    ]

                    total_tokens = event[
                        "total_tokens"
                    ]

                    estimated_cost = event[
                        "estimated_cost"
                    ]

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
# RENDER CONVERSATION
# =============================================================================

if (
    len(st.session_state.conversations)
    > 0
    and st.session_state.active_conversation
    is not None
):

    conversation = (
        st.session_state.conversations[
            st.session_state.active_conversation
        ]
    )

    # =========================================================================
    # LATEST MESSAGE FIRST
    # =========================================================================

    reversed_messages = list(
        enumerate(
            conversation["messages"]
        )
    )[::-1]

    for idx, message in reversed_messages:

        st.divider()

        render_user_message(
            message["question"]
        )

        st.divider()

        # ================================================================
        # SHOW CARDS ONLY FOR INITIAL QUERY
        # ================================================================

        if idx == 0:

            render_projection_cards(
                message["response"]
            )

            st.divider()

            render_recommended_plans(
                message["response"]
            )

            st.divider()

        # ================================================================
        # ASSISTANT RESPONSE
        # ================================================================

        render_assistant_message(
            message["response"][
                "generated_response"
            ]
        )

        st.divider()

        # ================================================================
        # SOURCES FOR EVERY RESPONSE
        # ================================================================

        render_sources(
            message["documents"]
        )

        st.divider()

        # ================================================================
        # FOOTER METRICS
        # ================================================================

        render_footer_metrics(
            message["response"],
            message["frontend_time"]
        )