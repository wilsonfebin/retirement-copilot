# =============================================================================
# backend/services/analysis_service.py
# =============================================================================

from app.rag.retriever import (
    retrieve_documents
)

from app.guardrails.retrieval_guard import (
    validate_retrieval
)

from app.agents.orchestrator import (
    detect_filters,
    build_context,
    extract_recommended_plans,
    stream_response
)

from backend.services.simulation_service import (
    simulate_retirement
)


# =============================================================================
# STREAM RETIREMENT ANALYSIS
# =============================================================================

def stream_retirement_analysis(request):

    # =========================================================================
    # RETRIEVAL
    # =========================================================================

    filters = detect_filters(
        request.query
    )

    documents = retrieve_documents(

        query=request.query,

        filters=filters,

        k=4
    )

    guardrail_result = (
        validate_retrieval(
            documents
        )
    )

    if not guardrail_result["is_valid"]:

        yield {

            "type": "error",

            "content":
                guardrail_result["reason"]
        }

        return

    retrieval_context = (
        build_context(
            documents
        )
    )

    recommended_plans = (
        extract_recommended_plans(
            documents
        )
    )

    # =========================================================================
    # DOCUMENT FORMATTING
    # =========================================================================

    unique_sources = {}

    for doc in documents:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        if source not in unique_sources:

            unique_sources[source] = {

                "source": source,

                "content":
                    doc.page_content[:1500]
            }

    formatted_documents = list(
        unique_sources.values()
    )

    # =========================================================================
    # SIMULATION
    # =========================================================================

    simulation_result = (
        simulate_retirement(
            request
        )
    )

    # =========================================================================
    # STREAM LLM RESPONSE
    # =========================================================================

    full_response = ""

    final_metrics = {

        "backend_time": 0,

        "prompt_tokens": 0,

        "completion_tokens": 0,

        "total_tokens": 0,

        "estimated_cost": 0
    }

    for event in stream_response(

        query=request.query,

        retrieval_context=
            retrieval_context,

        simulation_result=
            simulation_result,

        conversation_history=""
    ):

        # =====================================================================
        # TOKEN STREAM
        # =====================================================================

        if event["type"] == "content":

            full_response += (
                event["chunk"]
            )

            yield {

                "type": "token",

                "content":
                    event["chunk"]
            }

        # =====================================================================
        # FINAL METRICS
        # =====================================================================

        elif event["type"] == "complete":

            final_metrics = {

                "backend_time":
                    event.get(
                        "backend_time",
                        0
                    ),

                "prompt_tokens":
                    event.get(
                        "prompt_tokens",
                        0
                    ),

                "completion_tokens":
                    event.get(
                        "completion_tokens",
                        0
                    ),

                "total_tokens":
                    event.get(
                        "total_tokens",
                        0
                    ),

                "estimated_cost":
                    event.get(
                        "estimated_cost",
                        0
                    )
            }

    # =========================================================================
    # FINAL EVENT
    # =========================================================================

    yield {

        "type": "complete",

        "full_response":
            full_response,

        "recommended_plans":
            recommended_plans,

        "documents":
            formatted_documents,

        "backend_time":
            final_metrics[
                "backend_time"
            ],

        "prompt_tokens":
            final_metrics[
                "prompt_tokens"
            ],

        "completion_tokens":
            final_metrics[
                "completion_tokens"
            ],

        "total_tokens":
            final_metrics[
                "total_tokens"
            ],

        "estimated_cost":
            final_metrics[
                "estimated_cost"
            ]
    }