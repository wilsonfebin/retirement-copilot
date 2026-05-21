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

    ragas_metrics = response.get(

        "ragas_metrics"

    )

    if ragas_metrics:

        st.markdown(

            "### 🧠 AI Quality Metrics"

        )

        metric_col1, metric_col2, metric_col3 = (

            st.columns(3)

        )

        with metric_col1:

            st.metric(

                "Groundedness",

                f"{ragas_metrics.get('groundedness', 0)}%"

            )

        with metric_col2:

            st.metric(

                "Answer Relevance",

                f"{ragas_metrics.get('answer_relevance', 0)}%"

            )

        with metric_col3:

            st.metric(

                "Hallucination Risk",

                ragas_metrics.get(

                    "hallucination_risk",

                    "Unknown"

                )

            )