# =============================================================================
# app/ui/charts.py
# =============================================================================

import pandas as pd
import plotly.graph_objects as go
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
# CORPUS GROWTH CHART
# =============================================================================

def render_corpus_growth_chart(

    simulation_result,

    risk_profile,

    annual_return,

    monthly_investment,

    retirement_age,

    target_monthly_income=None,

    withdrawal_rate=0.04
):

    # =========================================================================
    # RISK COLORS
    # =========================================================================

    risk_colors = {

        "low": "#5ee36a",

        "moderate": "#4da3ff",

        "high": "#ff914d"
    }

    line_color = risk_colors.get(
        risk_profile,
        "#5ee36a"
    )

    # =========================================================================
    # TARGET CORPUS
    # =========================================================================

    required_corpus = None

    if target_monthly_income:

        required_corpus = (

            target_monthly_income
            * 12

        ) / withdrawal_rate

    # =========================================================================
    # PROJECTION DATA
    # =========================================================================

    projection_points = simulation_result[
        "projection_points"
    ]

    ages = [

        point["age"]

        for point in projection_points
    ]

    corpus_values = [

        point["corpus"]

        for point in projection_points
    ]

    # =========================================================================
    # DATAFRAME
    # =========================================================================

    df = pd.DataFrame({

        "Age":
            ages,

        "Projected Corpus":
            corpus_values
    })

    # =========================================================================
    # FINAL CORPUS
    # =========================================================================

    final_corpus = simulation_result[
        "projected_corpus"
    ]

    # =========================================================================
    # RETIREMENT GAP
    # =========================================================================

    retirement_gap = 0

    if required_corpus:

        retirement_gap = max(

            required_corpus
            - final_corpus,

            0
        )

    # =========================================================================
    # CHART
    # =========================================================================

    fig = go.Figure()

    # =========================================================================
    # PROJECTION LINE
    # =========================================================================

    fig.add_trace(

        go.Scatter(

            x=df["Age"],

            y=df["Projected Corpus"],

            mode="lines+markers",

            name=f"{risk_profile.title()} Risk Projection",

            line=dict(

                color=line_color,

                width=4
            ),

            marker=dict(
                size=7
            ),

            fill="tozeroy",

            fillcolor="rgba(94,227,106,0.10)"
        )
    )

    # =========================================================================
    # TARGET LINE
    # =========================================================================

    if required_corpus:

        fig.add_hline(

            y=required_corpus,

            line_dash="dash",

            line_color="#ff5c5c",

            annotation_text=(
                f"Target Corpus "
                f"({format_indian_currency(required_corpus)})"
            ),

            annotation_position="top right"
        )

    # =========================================================================
    # FINAL PROJECTION LABEL
    # =========================================================================

    fig.add_annotation(

        x=retirement_age,

        y=final_corpus,

        text=(
            f"""
Projected at {retirement_age}<br>
<b>{format_indian_currency(final_corpus)}</b>
"""
        ),

        showarrow=True,

        arrowhead=2,

        bgcolor="#111827",

        bordercolor="#334155",

        font=dict(

            size=13,

            color="white"
        )
    )

    # =========================================================================
    # RETIREMENT GAP
    # =========================================================================

    if required_corpus and retirement_gap > 0:

        fig.add_annotation(

            x=retirement_age - 5,

            y=required_corpus * 0.82,

            text=(
                f"""
Retirement Gap<br>
<b>{format_indian_currency(retirement_gap)}</b>
"""
            ),

            showarrow=True,

            arrowhead=2,

            bgcolor="#111827",

            bordercolor="#334155",

            font=dict(

                size=14,

                color="white"
            )
        )

    # =========================================================================
    # LAYOUT
    # =========================================================================

    fig.update_layout(

        title=dict(

            text="Projected Retirement Corpus Growth",

            font=dict(

                size=24,

                color="white"
            )
        ),

        paper_bgcolor="#081325",

        plot_bgcolor="#081325",

        font=dict(
            color="white"
        ),

        xaxis=dict(

            title="Age",

            gridcolor="rgba(255,255,255,0.06)",

            zeroline=False
        ),

        yaxis=dict(

            title="Corpus (₹)",

            gridcolor="rgba(255,255,255,0.06)",

            zeroline=False,

            tickformat=","
        ),

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.02,

            xanchor="right",

            x=1
        ),

        height=540,

        margin=dict(

            l=20,

            r=20,

            t=80,

            b=20
        ),

        hovermode="x unified"
    )

    # =========================================================================
    # RENDER
    # =========================================================================

    st.plotly_chart(

        fig,

        use_container_width=True
    )

    # =========================================================================
    # FOOTER ASSUMPTIONS
    # =========================================================================

    st.markdown(

        f"""
<div style="
margin-top:-10px;
margin-bottom:10px;
font-size:18px;
color:#94A3B8;
text-align:center;
">

Target Corpus Assumptions •
Monthly SIP:
<b>{format_indian_currency(monthly_investment)}</b>
•
Withdrawal Rate:
<b>{withdrawal_rate*100:.0f}%</b>
•
Annual Return:
<b>{annual_return*100:.0f}%</b>
•
Risk Profile:
<b>{risk_profile.title()}</b>

</div>
""",

        unsafe_allow_html=True
    )