# =============================================================================
# app/api/analysis_client.py
# =============================================================================

import json
import requests
import streamlit as st


# =============================================================================
# API CONFIG
# =============================================================================

API_BASE_URL = st.secrets[
    "BACKEND_URL"
]


# =============================================================================
# STREAM RETIREMENT ANALYSIS
# =============================================================================

def stream_retirement_analysis(

    query,

    current_age,

    retirement_age,

    current_corpus,

    monthly_investment,

    risk_profile,

    annual_return
):

    payload = {

        "query":
            query,

        "current_age":
            current_age,

        "retirement_age":
            retirement_age,

        "current_corpus":
            current_corpus,

        "monthly_investment":
            monthly_investment,

        "risk_profile":
            risk_profile,

        "annual_return":
            annual_return
    }

    response = requests.post(

        f"{API_BASE_URL}/analyze-stream",

        json=payload,

        stream=True,

        timeout=300
    )

    response.raise_for_status()

    # =========================================================================
    # SSE STREAM PARSING
    # =========================================================================

    for line in response.iter_lines(

        decode_unicode=True
    ):

        if not line:

            continue

        if line.startswith(
            "data: "
        ):

            try:

                json_data = line.replace(

                    "data: ",

                    ""
                )

                parsed_event = json.loads(
                    json_data
                )

                yield parsed_event

            except Exception:

                continue