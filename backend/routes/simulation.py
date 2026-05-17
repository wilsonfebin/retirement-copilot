from fastapi import APIRouter

from backend.models.simulation_models import (
    SimulationRequest
)

from backend.services.simulation_service import (
    simulate_retirement
)

router = APIRouter()


@router.post("/simulate")
def simulate(request: SimulationRequest):

    return simulate_retirement(request)
