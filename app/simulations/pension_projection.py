def future_value_lumpsum(
    principal,
    annual_return,
    years
):

    return principal * ((1 + annual_return) ** years)


def future_value_sip(
    monthly_investment,
    annual_return,
    years
):

    monthly_rate = annual_return / 12

    months = years * 12

    future_value = (
        monthly_investment *
        (
            ((1 + monthly_rate) ** months - 1)
            / monthly_rate
        ) *
        (1 + monthly_rate)
    )

    return future_value


def calculate_retirement_corpus(
    current_corpus,
    monthly_investment,
    annual_return,
    years_to_retirement
):

    future_lumpsum = future_value_lumpsum(
        principal=current_corpus,
        annual_return=annual_return,
        years=years_to_retirement
    )

    future_sip = future_value_sip(
        monthly_investment=monthly_investment,
        annual_return=annual_return,
        years=years_to_retirement
    )

    total_corpus = future_lumpsum + future_sip

    return {
        "future_lumpsum": round(future_lumpsum),
        "future_sip": round(future_sip),
        "total_corpus": round(total_corpus)
    }


def estimate_monthly_pension(
    corpus,
    withdrawal_rate=0.06
):

    annual_income = corpus * withdrawal_rate

    monthly_income = annual_income / 12

    return round(monthly_income)