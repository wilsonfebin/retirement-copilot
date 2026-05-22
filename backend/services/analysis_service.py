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

from app.observability.phoenix_config import (
    otel_tracer
)


# =============================================================================
# STREAM RETIREMENT ANALYSIS
# =============================================================================

def stream_retirement_analysis(request):

    with otel_tracer.start_as_current_span(

        "stream_retirement_analysis"

    ) as span:

        # =====================================================================
        # QUERY METRICS
        # =====================================================================

        span.set_attribute(

            "query.text",

            request.query[:500]
        )

        span.set_attribute(

            "query.length",

            len(request.query)
        )

        # =====================================================================
        # CONVERSATION METRICS
        # =====================================================================

        conversation_history = ""

        span.set_attribute(

            "conversation.turn_count",

            0
        )

        # =====================================================================
        # RETRIEVAL
        # =====================================================================

        filters = detect_filters(
            request.query
        )

        span.set_attribute(

            "retrieval.has_filters",

            bool(filters)
        )

        documents = retrieve_documents(

            query=request.query,

            filters=filters,

            k=4
        )

        span.set_attribute(

            "retrieval.document_count",

            len(documents)
        )

        guardrail_result = (
            validate_retrieval(
                documents
            )
        )

        span.set_attribute(

            "guardrail.retrieval_valid",

            guardrail_result["is_valid"]
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

        # =====================================================================
        # RETRIEVAL CONTEXT METRICS
        # =====================================================================

        span.set_attribute(

            "retrieval.context_chars",

            len(retrieval_context)
        )

        recommended_plans = (
            extract_recommended_plans(
                documents
            )
        )

        # =====================================================================
        # DOCUMENT SOURCES
        # =====================================================================

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

        source_names = [

            doc["source"]

            for doc in formatted_documents
        ]

        span.set_attribute(

            "retrieval.sources",

            str(source_names)
        )

        # =====================================================================
        # SIMULATION
        # =====================================================================

        simulation_result = (
            simulate_retirement(
                request
            )
        )

        span.set_attribute(

            "simulation.current_age",

            request.current_age
        )

        span.set_attribute(

            "simulation.retirement_age",

            request.retirement_age
        )

        span.set_attribute(

            "simulation.risk_profile",

            request.risk_profile
        )

        # =====================================================================
        # LLM METRICS
        # =====================================================================

        span.set_attribute(

            "llm.model",

            "gpt-4o-mini"
        )

        # =====================================================================
        # STREAM LLM RESPONSE
        # =====================================================================

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

            conversation_history=
                conversation_history
        ):

            # ================================================================
            # TOKEN STREAM
            # ================================================================

            if event["type"] == "content":

                full_response += (
                    event["chunk"]
                )

                yield {

                    "type": "token",

                    "content":
                        event["chunk"]
                }

            # ================================================================
            # FINAL METRICS
            # ================================================================

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

        # =====================================================================
        # LLM TELEMETRY
        # =====================================================================

        span.set_attribute(

            "llm.prompt_tokens",

            final_metrics[
                "prompt_tokens"
            ]
        )

        span.set_attribute(

            "llm.completion_tokens",

            final_metrics[
                "completion_tokens"
            ]
        )

        span.set_attribute(

            "llm.total_tokens",

            final_metrics[
                "total_tokens"
            ]
        )

        span.set_attribute(

            "llm.cost",

            final_metrics[
                "estimated_cost"
            ]
        )

        # =====================================================================
        # RESPONSE METRICS
        # =====================================================================

        span.set_attribute(

            "streaming.response_length",

            len(full_response)
        )

        span.set_attribute(

            "backend.latency_seconds",

            final_metrics[
                "backend_time"
            ]
        )

        # =====================================================================
        # FINAL EVENT
        # =====================================================================

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