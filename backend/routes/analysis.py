# =============================================================================
# backend/routes/analysis.py
# =============================================================================

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.models.analysis_models import (
    AnalysisRequest
)

from backend.services.analysis_service import (
    stream_retirement_analysis
)

import json


router = APIRouter()


# =============================================================================
# STREAM ANALYSIS
# =============================================================================

@router.post("/analyze-stream")

def analyze_stream(request: AnalysisRequest):

    def event_generator():

        for event in stream_retirement_analysis(
            request
        ):

            yield (
                json.dumps(event)
                + "\n"
            )

    return StreamingResponse(

        event_generator(),

        media_type="application/json"
    )