from app.simulations.pension_projection import (
    calculate_retirement_corpus,
    estimate_monthly_pension
)

from app.observability.traces import logger


def classify_retirement_readiness(monthly_pension):

    if monthly_pension >= 150000:
        return "strong"

    elif monthly_pension >= 80000:
        return "moderate"

    return "weak"


def run_retirement_simulation(
    current_age,
    retirement_age,
    current_corpus,
    monthly_investment,
    annual_return=0.10
):

    logger.info("Starting retirement simulation")

    years_to_retirement = retirement_age - current_age

    logger.info(f"Years to retirement: {years_to_retirement}")

    projection = calculate_retirement_corpus(
        current_corpus=current_corpus,
        monthly_investment=monthly_investment,
        annual_return=annual_return,
        years_to_retirement=years_to_retirement
    )

    monthly_pension = estimate_monthly_pension(
        corpus=projection["total_corpus"]
    )

    readiness = classify_retirement_readiness(
        monthly_pension=monthly_pension
    )

    simulation_result = {
        "current_age": current_age,
        "retirement_age": retirement_age,
        "years_to_retirement": years_to_retirement,
        "current_corpus": current_corpus,
        "monthly_investment": monthly_investment,
        "projected_corpus": projection["total_corpus"],
        "future_lumpsum_value": projection["future_lumpsum"],
        "future_sip_value": projection["future_sip"],
        "estimated_monthly_pension": monthly_pension,
        "retirement_readiness": readiness
    }

    logger.info(f"Simulation result: {simulation_result}")

    return simulation_result