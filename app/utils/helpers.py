def format_retirement_response(
    simulation_result,
    recommended_plans,
    generated_response
):

    formatted_response = {

        "retirement_readiness":
            simulation_result.get("retirement_readiness"),

        "projected_corpus":
            simulation_result.get("projected_corpus"),

        "estimated_monthly_pension":
            simulation_result.get("estimated_monthly_pension"),

        "future_lumpsum_value":
            simulation_result.get("future_lumpsum_value"),

        "future_sip_value":
            simulation_result.get("future_sip_value"),

        "recommended_plans":
            recommended_plans,

        "generated_response":
            generated_response
    }

    return formatted_response