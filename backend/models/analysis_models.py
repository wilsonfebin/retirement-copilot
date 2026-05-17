# =============================================================================
# backend/models/analysis_models.py
# =============================================================================

from pydantic import BaseModel


# =============================================================================
# ANALYSIS REQUEST
# =============================================================================

class AnalysisRequest(BaseModel):

    query: str

    current_age: int

    retirement_age: int

    current_corpus: float

    monthly_investment: float

    risk_profile: str

    annual_return: float