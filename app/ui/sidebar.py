import streamlit as st


def render_knowledge_modules():

    st.sidebar.divider()

    st.sidebar.subheader(

        "📚 Knowledge Modules"

    )

    modules = [

        "Smart Pension Plan",

        "Systematic Retirement Plan",

        "Personal Pension Plus",

        "Retirement Savings Fund"

    ]

    for module in modules:

        st.sidebar.caption(

            f"• {module}"

        )

def render_ai_evaluation_toggle():

    st.sidebar.divider()

    st.sidebar.subheader(

        "🧪 AI Evaluation"

    )

    enable_ragas = st.sidebar.toggle(

        "Enable RAGAS Evaluation",

        value=False,

        key="ragas_eval_toggle"

    )

    return enable_ragas

def render_chat_history():

    st.sidebar.divider()

    st.sidebar.subheader("💬 Conversations")

    if len(st.session_state.conversations) == 0:

        st.sidebar.caption(
            "No conversations yet"
        )

        return

    for idx, conversation in enumerate(
        st.session_state.conversations
    ):

        col1, col2 = st.sidebar.columns([5, 1])

        title = conversation["title"]

        with col1:

            active = (
                st.session_state.active_conversation
                == idx
            )

            button_type = (
                "primary"
                if active
                else "secondary"
            )

            if st.button(
                title,
                key=f"conversation_{idx}",
                width="stretch",
                type=button_type
            ):

                st.session_state.active_conversation = idx

                st.rerun()

        with col2:

            if st.button(
                "🗑",
                key=f"delete_{idx}",
                use_container_width=True
            ):

                st.session_state.conversations.pop(idx)

                if (
                    len(st.session_state.conversations)
                    == 0
                ):

                    st.session_state.active_conversation = None

                else:

                    st.session_state.active_conversation = (
                        len(st.session_state.conversations) - 1
                    )

                st.rerun()


def render_chat_controls():

    st.sidebar.divider()
    st.sidebar.subheader(

        "⚙️ Controls"

    )

    if st.sidebar.button(

        "➕ New Chat",

        width="stretch"

    ):

        new_chat = {

            "title": "New Chat",

            "messages": []

        }

        st.session_state.conversations.append(

            new_chat

        )

        st.session_state.active_conversation = (

            len(

                st.session_state.conversations

            ) - 1

        )

        st.rerun()

    if st.sidebar.button(

        "🧹 Clear Conversations",

        width="stretch"

    ):

        st.session_state.conversations = []

        st.session_state.active_conversation = None

        st.rerun()

    st.sidebar.divider()

    return enable_ragas
