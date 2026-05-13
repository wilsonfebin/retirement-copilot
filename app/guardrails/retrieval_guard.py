# =============================================================================
# app/guardrails/retrieval_guard.py
# =============================================================================

MIN_DOCUMENTS = 2

MIN_TOTAL_CONTENT_LENGTH = 400


def validate_retrieval(documents):

    # =========================================================================
    # NO DOCUMENTS
    # =========================================================================

    if not documents:

        return {
            "is_valid": False,
            "reason":
                "No relevant pension documents found."
        }

    # =========================================================================
    # DOCUMENT COUNT CHECK
    # =========================================================================

    if len(documents) < MIN_DOCUMENTS:

        return {
            "is_valid": False,
            "reason":
                "Insufficient pension document coverage."
        }

    # =========================================================================
    # CONTENT LENGTH CHECK
    # =========================================================================

    total_content = ""

    for doc in documents:

        total_content += doc.page_content

    if len(total_content.strip()) < MIN_TOTAL_CONTENT_LENGTH:

        return {
            "is_valid": False,
            "reason":
                "Retrieved pension content is too limited."
        }

    # =========================================================================
    # VALID
    # =========================================================================

    return {
        "is_valid": True,
        "reason": None
    }
