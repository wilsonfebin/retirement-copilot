# =============================================================================
# app/evaluation/ragas_evaluator.py
# =============================================================================

from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy
)

from langchain_openai import (
    ChatOpenAI,
    OpenAIEmbeddings
)

from observability.phoenix_config import (
    tracer
)

from opentelemetry.trace import (
    get_current_span
)


# =============================================================================
# EVALUATOR MODELS
# =============================================================================

evaluator_llm = ChatOpenAI(

    model="gpt-4o-mini",

    temperature=0
)

evaluator_embeddings = (
    OpenAIEmbeddings()
)


# =============================================================================
# RAGAS EVALUATION
# =============================================================================

@tracer.chain
def evaluate_response(

    query,
    retrieved_context,
    generated_response
):

    try:

        # =============================================================
        # ACTIVE SPAN
        # =============================================================

        span = get_current_span()

        # =============================================================
        # INPUT METRICS
        # =============================================================

        span.set_attribute(

            "ragas.query",

            query[:500]
        )

        span.set_attribute(

            "ragas.query_length",

            len(query)
        )

        span.set_attribute(

            "ragas.response_length",

            len(generated_response)
        )

        span.set_attribute(

            "ragas.context_length",

            len(retrieved_context)
        )

        # =============================================================
        # TRUNCATE CONTEXT
        # =============================================================

        truncated_context = (

            retrieved_context[:1500]
        )

        span.set_attribute(

            "ragas.truncated_context_length",

            len(truncated_context)
        )

        # =============================================================
        # DATASET
        # =============================================================

        dataset = Dataset.from_dict(

            {

                "question": [

                    query
                ],

                "answer": [

                    generated_response
                ],

                "contexts": [[

                    truncated_context
                ]]
            }
        )

        # =============================================================
        # RUN EVALUATION
        # =============================================================

        result = evaluate(

            dataset=dataset,

            metrics=[

                faithfulness,
                answer_relevancy
            ],

            llm=evaluator_llm,

            embeddings=evaluator_embeddings
        )

        # =============================================================
        # DEBUG LOGS
        # =============================================================

        print(
            "RAGAS RESULT:"
        )

        print(result)

        print(
            type(result)
        )

        # =============================================================
        # CONVERT TO PANDAS
        # =============================================================

        scores = result.to_pandas()

        print(
            scores
        )

        # =============================================================
        # EXTRACT SCORES
        # =============================================================

        faithfulness_score = round(

            float(

                scores[
                    "faithfulness"
                ][0]

            ) * 100
        )

        relevancy_score = round(

            float(

                scores[
                    "answer_relevancy"
                ][0]

            ) * 100
        )

        # =============================================================
        # HALLUCINATION RISK
        # =============================================================

        if faithfulness_score >= 90:

            hallucination_risk = "Low"

        elif faithfulness_score >= 75:

            hallucination_risk = "Moderate"

        else:

            hallucination_risk = "High"

        # =============================================================
        # RAGAS TELEMETRY
        # =============================================================

        span.set_attribute(

            "ragas.groundedness",

            faithfulness_score
        )

        span.set_attribute(

            "ragas.answer_relevance",

            relevancy_score
        )

        span.set_attribute(

            "ragas.hallucination_risk",

            hallucination_risk
        )

        span.set_attribute(

            "ragas.evaluation_success",

            True
        )

        # =============================================================
        # RETURN
        # =============================================================

        return {

            "groundedness":
                faithfulness_score,

            "answer_relevance":
                relevancy_score,

            "hallucination_risk":
                hallucination_risk
        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        print(
            f"Ragas evaluation failed: {e}"
        )

        # =============================================================
        # FAILURE TELEMETRY
        # =============================================================

        span = get_current_span()

        span.set_attribute(

            "ragas.evaluation_success",

            False
        )

        span.set_attribute(

            "ragas.error",

            str(e)
        )

        return {

            "groundedness": 0,

            "answer_relevance": 0,

            "hallucination_risk": "Unknown"
        }