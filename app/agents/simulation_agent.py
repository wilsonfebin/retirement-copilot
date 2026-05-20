# =============================================================================
# app/agents/simulation_agent.py
# =============================================================================

from app.simulations.pension_projection import (
    calculate_retirement_corpus,
    estimate_monthly_pension
)

from app.observability.traces import logger


# =============================================================================
# READINESS CLASSIFICATION
# =============================================================================

def classify_retirement_readiness(monthly_pension):

    if monthly_pension >= 100000:

        return "strong"

    elif monthly_pension >= 50000:

        return "moderate"

    return "weak"


# =============================================================================
# RETIREMENT SIMULATION
# =============================================================================

def run_retirement_simulation(

    current_age,

    retirement_age,

    current_corpus,

    monthly_investment,

    annual_return=0.10
):

    years_to_retirement = (
        retirement_age - current_age
    )

    # =========================================================================
    # MAIN PROJECTION
    # =========================================================================

    projection = calculate_retirement_corpus(

        current_corpus=current_corpus,

        monthly_investment=monthly_investment,

        annual_return=annual_return,

        years_to_retirement=years_to_retirement
    )

    # =========================================================================
    # MONTHLY PENSION
    # =========================================================================

    monthly_pension = estimate_monthly_pension(

        corpus=projection["total_corpus"]
    )

    # =========================================================================
    # READINESS
    # =========================================================================

    readiness = classify_retirement_readiness(

        monthly_pension=monthly_pension
    )

    # =========================================================================
    # PROJECTION SERIES
    # =========================================================================

    projection_points = []

    running_corpus = current_corpus

    monthly_rate = (
        annual_return / 12
    )

    current_projection_age = current_age

    for year in range(

        1,

        years_to_retirement + 1
    ):

        for month in range(12):

            running_corpus = (

                running_corpus
                *
                (1 + monthly_rate)

            ) + monthly_investment

        current_projection_age += 1

        projection_points.append(

            {
                "age":
                    current_projection_age,

                "corpus":
                    round(running_corpus)
            }
        )

    # =========================================================================
    # FINAL RESPONSE
    # =========================================================================

    simulation_result = {

        "current_age":
            current_age,

        "retirement_age":
            retirement_age,

        "years_to_retirement":
            years_to_retirement,

        "current_corpus":
            current_corpus,

        "monthly_investment":
            monthly_investment,

        "projected_corpus":
            projection["total_corpus"],

        "future_lumpsum_value":
            projection["future_lumpsum"],

        "future_sip_value":
            projection["future_sip"],

        "estimated_monthly_pension":
            monthly_pension,

        "retirement_readiness":
            readiness,

        "projection_points":
            projection_points
    }


    return simulation_result