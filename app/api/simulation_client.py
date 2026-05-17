# =============================================================================
# app/api/simulation_client.py
# =============================================================================

import requests


# =============================================================================
# API CONFIG
# =============================================================================

import streamlit as st

API_BASE_URL = st.secrets["BACKEND_URL"]

# =============================================================================
# RETIREMENT SIMULATION API
# =============================================================================

def get_retirement_simulation(

    current_age,

    retirement_age,

    current_corpus,

    monthly_investment,

    annual_return
):

    payload = {

        "current_age":
            current_age,

        "retirement_age":
            retirement_age,

        "current_corpus":
            current_corpus,

        "monthly_investment":
            monthly_investment,

        "annual_return":
            annual_return
    }

    response = requests.post(

        f"{API_BASE_URL}/simulate",

        json=payload,

        timeout=30
    )

    response.raise_for_status()

    return response.json()