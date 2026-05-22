# =============================================================================
# app/api/simulation_client.py
# =============================================================================

from agents.simulation_agent import (
    run_retirement_simulation
)

from backend.models.simulation_models import (
    SimulationRequest
)


# =============================================================================
# GET RETIREMENT SIMULATION
# =============================================================================

# =============================================================================
# GET RETIREMENT SIMULATION
# =============================================================================

def get_retirement_simulation(

    current_age,

    retirement_age,

    current_corpus,

    monthly_investment,

    annual_return
):

    simulation_result = run_retirement_simulation(

        current_age=current_age,

        retirement_age=retirement_age,

        current_corpus=current_corpus,

        monthly_investment=monthly_investment,

        annual_return=annual_return
    )

    return simulation_result