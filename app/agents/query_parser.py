# =============================================================================
# app/agents/query_parser.py
# =============================================================================

import re


def extract_financial_targets(query):

    extracted = {

        "target_pension": None,

        "target_corpus": None
    }

    # =========================================================================
    # NORMALIZE QUERY
    # =========================================================================

    query_lower = query.lower()

    # =========================================================================
    # SUPPORTED PATTERNS
    # =========================================================================

    patterns = [

        # 1L
        r'(\d+(?:\.\d+)?)\s*(l|lakh)',

        # 1L pension
        r'(\d+(?:\.\d+)?)\s*(l|lakh)\s*(monthly)?\s*(pension|income)',

        # 25000 pension
        r'(\d+(?:\.\d+)?)\s*(monthly)?\s*(pension|income)',

        # pension of 1L
        r'(pension|income).*?(\d+(?:\.\d+)?)\s*(l|lakh)?'
    ]

    # =========================================================================
    # PATTERN MATCHING
    # =========================================================================

    for pattern in patterns:

        match = re.search(
            pattern,
            query_lower
        )

        if match:

            # ================================================================
            # EXTRACT NUMBERS
            # ================================================================

            numbers = re.findall(
                r'\d+(?:\.\d+)?',
                match.group()
            )

            if numbers:

                value = float(numbers[0])

                # ============================================================
                # LAKH CONVERSION
                # ============================================================

                if (
                    "l" in match.group()
                    or
                    "lakh" in match.group()
                ):

                    value *= 100000

                extracted[
                    "target_pension"
                ] = int(value)

                break

    return extracted