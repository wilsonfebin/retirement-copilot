from backend.models.analysis_models import (
    AnalysisRequest
)

from backend.services.analysis_service import (
    stream_retirement_analysis
)


def stream_retirement_analysis_local(

    query,

    current_age,

    retirement_age,

    current_corpus,

    monthly_investment,

    risk_profile,

    annual_return
):

    request = AnalysisRequest(

        query=query,

        current_age=current_age,

        retirement_age=retirement_age,

        current_corpus=current_corpus,

        monthly_investment=monthly_investment,

        risk_profile=risk_profile,

        annual_return=annual_return
    )

    for event in stream_retirement_analysis(
        request
    ):

        yield event