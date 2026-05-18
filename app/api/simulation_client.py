# =============================================================================
# app/api/simulation_client.py
# =============================================================================

from backend.services.simulation_service import (
    simulate_retirement
)

from backend.models.simulation_models import (
    SimulationRequest
)


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

    request = SimulationRequest(

        current_age=current_age,

        retirement_age=retirement_age,

        current_corpus=current_corpus,

        monthly_investment=monthly_investment,

        annual_return=annual_return
    )

    simulation_result = simulate_retirement(
        request
    )

    return simulation_result