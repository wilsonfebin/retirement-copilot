# =============================================================================
# app/ui/chat.py
# =============================================================================

import streamlit as st


# =============================================================================
# USER MESSAGE
# =============================================================================

def render_user_message(question):

    st.markdown(

        f"""
<div class="user-question-card">

<div style="
display:flex;
align-items:center;
justify-content:space-between;
margin-bottom:10px;
">

<div style="
font-size:14px;
font-weight:600;
color:#93C5FD;
letter-spacing:0.03em;
text-transform:uppercase;
">
Your Question
</div>

<div style="
background:rgba(59,130,246,0.15);
padding:6px 10px;
border-radius:999px;
font-size:12px;
color:#BFDBFE;
font-weight:600;
">
Retirement Query
</div>

</div>

<div class="user-question-text">
{question}
</div>

</div>
""",

        unsafe_allow_html=True
    )


# =============================================================================
# ASSISTANT MESSAGE
# =============================================================================

def render_assistant_message(response):

    st.markdown(

        """
<div style="
display:flex;
align-items:center;
justify-content:space-between;
margin-top:10px;
margin-bottom:14px;
">

<div style="
font-size:24px;
font-weight:700;
color:white;
">
🤖 AI Retirement Insights
</div>

<div style="
background:rgba(34,197,94,0.12);
border:1px solid rgba(34,197,94,0.22);
padding:6px 12px;
border-radius:999px;
font-size:12px;
font-weight:600;
color:#86EFAC;
">
Grounded Response
</div>

</div>
""",

        unsafe_allow_html=True
    )

    # =========================================================================
    # RESPONSE CONTAINER
    # =========================================================================

    st.markdown(
        response
    )