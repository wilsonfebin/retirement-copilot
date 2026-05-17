# =============================================================================
# app/api/analysis_client.py
# =============================================================================

import requests
import json


BASE_URL = "http://127.0.0.1:8000"


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

        f"{BASE_URL}/analyze-stream",

        json=payload,

        stream=True
    )

    response.raise_for_status()

    for line in response.iter_lines():

        if line:

            yield json.loads(
                line.decode("utf-8")
            )