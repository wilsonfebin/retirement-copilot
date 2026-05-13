import streamlit as st


def render_user_message(question):

    st.subheader("❓ Your Question")

    st.markdown(
        f"""
<div class="user-question-card">
    <div class="user-question-text">
        {question}
    </div>
</div>
""",
        unsafe_allow_html=True
    )


def render_assistant_message(response):

    st.subheader("🤖 AI Retirement Insights")

    st.markdown(
        f"""
<div class="assistant-card">
    {response}
</div>
""",
        unsafe_allow_html=True
    )
