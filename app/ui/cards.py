# =============================================================================
# app/ui/cards.py
# =============================================================================

import streamlit as st


# =============================================================================
# INDIAN NUMBER FORMAT
# =============================================================================

def format_indian_currency(value):

    value = int(value)

    if value >= 10000000:

        return f"₹{value/10000000:.2f}Cr"

    if value >= 100000:

        return f"₹{value/100000:.1f}L"

    return f"₹{value:,}"


# =============================================================================
# PROJECTION CARDS
# =============================================================================

def render_projection_cards(response):

    st.markdown(
        "## 📊 Retirement Projection Dashboard"
    )

    projected_corpus = response[
        "projected_corpus"
    ]

    retirement_income = response[
        "estimated_monthly_pension"
    ]

    readiness = response[
        "retirement_readiness"
    ].title()

    # =========================================================================
    # READINESS COLORS
    # =========================================================================

    readiness_colors = {

        "Weak": "#f59e0b",

        "Moderate": "#3b82f6",

        "Strong": "#22c55e"
    }

    readiness_color = readiness_colors.get(
        readiness,
        "#22c55e"
    )

    # =========================================================================
    # CARD LAYOUT
    # =========================================================================

    col1, col2, col3 = st.columns(3)

    # =========================================================================
    # CARD 1
    # =========================================================================

    with col1:

        st.markdown(

            f"""
<div style="
background:linear-gradient(135deg,#081325,#0b1830);
border:1px solid rgba(255,255,255,0.06);
border-radius:18px;
padding:24px;
min-height:190px;
box-shadow:0 10px 30px rgba(0,0,0,0.35);
">

<div style="
font-size:18px;
font-weight:600;
color:#E2E8F0;
margin-bottom:22px;
">
Projected Corpus at Retirement
</div>

<div style="
font-size:52px;
font-weight:800;
color:#22c55e;
line-height:1;
margin-bottom:18px;
">
{format_indian_currency(projected_corpus)}
</div>

<div style="
font-size:15px;
color:#CBD5E1;
line-height:1.7;
">
Projected retirement corpus.
</div>

</div>
""",

            unsafe_allow_html=True
        )

    # =========================================================================
    # CARD 2
    # =========================================================================

    with col2:

        st.markdown(

            f"""
<div style="
background:linear-gradient(135deg,#081325,#0b1830);
border:1px solid rgba(255,255,255,0.06);
border-radius:18px;
padding:24px;
min-height:190px;
box-shadow:0 10px 30px rgba(0,0,0,0.35);
">

<div style="
font-size:18px;
font-weight:600;
color:#E2E8F0;
margin-bottom:22px;
">
Estimated Monthly Retirement Income
</div>

<div style="
font-size:52px;
font-weight:800;
color:#3b82f6;
line-height:1;
margin-bottom:18px;
">
{format_indian_currency(retirement_income)}
</div>

<div style="
font-size:15px;
color:#CBD5E1;
line-height:1.7;
">
Estimated monthly retirement income.
</div>

</div>
""",

            unsafe_allow_html=True
        )

    # =========================================================================
    # CARD 3
    # =========================================================================

    with col3:

        st.markdown(

            f"""
<div style="
background:linear-gradient(135deg,#081325,#0b1830);
border:1px solid rgba(255,255,255,0.06);
border-radius:18px;
padding:24px;
min-height:190px;
box-shadow:0 10px 30px rgba(0,0,0,0.35);
">

<div style="
font-size:18px;
font-weight:600;
color:#E2E8F0;
margin-bottom:22px;
">
Retirement Readiness
</div>

<div style="
font-size:52px;
font-weight:800;
color:{readiness_color};
line-height:1;
margin-bottom:18px;
">
{readiness}
</div>

<div style="
font-size:15px;
color:#CBD5E1;
line-height:1.7;
">
Current retirement preparedness.
</div>

</div>
""",

            unsafe_allow_html=True
        )


# =============================================================================
# RECOMMENDED PLANS
# =============================================================================

def render_recommended_plans(response):

    st.subheader(
        "🏦 Recommended Pension Plans"
    )

    plans = response.get(
        "recommended_plans",
        []
    )

    if not plans:

        st.info(
            "No pension plans identified."
        )

        return

    for plan in plans:

        st.markdown(

    f"""
<div style="
background: linear-gradient(
90deg,
rgba(16,185,129,0.18),
rgba(34,197,94,0.10)
);
border:1px solid rgba(16,185,129,0.18);
border-radius:14px;
padding:16px 20px;
margin-bottom:12px;
">

<div style="
font-size:24px;
font-weight:700;
color:white;
margin-bottom:6px;
">

{plan}

</div>

<div style="
font-size:15px;
color:#CBD5E1;
line-height:1.4;
">

Recommended based on retrieved pension
documents and retirement profile.

</div>

</div>
""",

    unsafe_allow_html=True
    )


# =============================================================================
# SOURCES
# =============================================================================

def render_sources(documents):

    st.subheader(
        "📚 Retrieved Pension Sources"
    )

    if not documents:

        st.warning(
            "No supporting documents retrieved."
        )

        return

    for doc in documents:

        with st.expander(

            f"📄 {doc['source']}"
        ):

            st.markdown(
                doc["content"]
            )