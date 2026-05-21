# =============================================================================
# app/evaluation/ragas_evaluator.py
# =============================================================================

from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy
)


# =============================================================================
# EVALUATE RESPONSE
# =============================================================================

def evaluate_response(

    query,
    retrieved_context,
    generated_response
):

    try:

        dataset = Dataset.from_dict({

            "question": [query],

            "answer": [generated_response],

            "contexts": [[retrieved_context]]
        })

        result = evaluate(

            dataset,

            metrics=[

                faithfulness,

                answer_relevancy
            ]
        )

        scores = result.to_pandas().iloc[0]

        groundedness = round(

            scores["faithfulness"] * 100
        )

        answer_relevance = round(

            scores["answer_relevancy"] * 100
        )

        # =============================================================
        # HALLUCINATION RISK
        # =============================================================

        if groundedness >= 90:

            hallucination_risk = "Low"

        elif groundedness >= 70:

            hallucination_risk = "Moderate"

        else:

            hallucination_risk = "High"

        return {

            "groundedness":
                groundedness,

            "answer_relevance":
                answer_relevance,

            "hallucination_risk":
                hallucination_risk
        }

    except Exception as e:

        print(

            f"Ragas evaluation failed: {e}"
        )

        return {

            "groundedness": None,

            "answer_relevance": None,

            "hallucination_risk": "Unknown"
        }
