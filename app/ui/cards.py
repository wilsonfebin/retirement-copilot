import streamlit as st


def render_projection_cards(response):

    st.subheader("📊 Retirement Projection")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Projected Corpus",
        f"₹{response['projected_corpus']:,}"
    )

    col2.metric(
        "Monthly Pension",
        f"₹{response['estimated_monthly_pension']:,}"
    )

    col3.metric(
        "Readiness",
        response["retirement_readiness"].title()
    )


def render_recommended_plans(response):

    st.subheader(
        "🏦 Recommended Pension Plans"
    )

    for plan in response[
        "recommended_plans"
    ]:

        st.success(plan)


def render_sources(documents):

    st.subheader("📚 Retrieved Sources")

    for doc in documents:

        with st.expander(
            doc["source"]
        ):

            st.markdown(
                doc["content"]
            )
