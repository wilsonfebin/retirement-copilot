from pydantic import BaseModel


class SimulationRequest(BaseModel):

    current_age: int

    retirement_age: int

    current_corpus: float

    monthly_investment: float

    annual_return: float


class ProjectionPoint(BaseModel):

    age: int

    corpus: float


class SimulationResponse(BaseModel):

    projected_corpus: float

    estimated_monthly_pension: float

    retirement_readiness: str

    projection_points: list[ProjectionPoint]
