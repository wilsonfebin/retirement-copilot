def format_retirement_response(

    simulation_result,

    recommended_plans,

    generated_response,

    backend_time,

    prompt_tokens,

    completion_tokens,

    total_tokens,

    estimated_cost, 
    ragas_metrics=None
):

    return {

        "retirement_readiness":
            simulation_result[
                "retirement_readiness"
            ],

        "projected_corpus":
            simulation_result[
                "projected_corpus"
            ],

        "estimated_monthly_pension":
            simulation_result[
                "estimated_monthly_pension"
            ],

        "future_lumpsum_value":
            simulation_result[
                "future_lumpsum_value"
            ],

        "future_sip_value":
            simulation_result[
                "future_sip_value"
            ],

        "recommended_plans":
            recommended_plans,

        "generated_response":
            generated_response,

        "backend_time":
            backend_time,

        "prompt_tokens":
            prompt_tokens,

        "completion_tokens":
            completion_tokens,

        "total_tokens":
            total_tokens,

        "estimated_cost":
            estimated_cost,
        "ragas_metrics": 
            ragas_metrics
    }