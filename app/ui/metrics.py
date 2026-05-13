import streamlit as st


def render_footer_metrics(
    response,
    frontend_time
):

    st.markdown(
        f"""
<div style="
display:flex;
gap:24px;
flex-wrap:wrap;
align-items:center;
opacity:0.75;
font-size:13px;
padding-top:8px;
padding-bottom:8px;
">

<span>
⚡ Backend: {response.get('backend_time', 0)}s
</span>

<span>
🖥️ Frontend: {frontend_time}s
</span>

<span>
🧠 Tokens: {response.get('total_tokens', 0)}
</span>

<span>
💲 Cost: ${response.get('estimated_cost', 0)}
</span>

</div>
""",
        unsafe_allow_html=True
    )