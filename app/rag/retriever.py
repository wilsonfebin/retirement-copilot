# =============================================================================
# app/rag/retriever.py
# =============================================================================

from app.rag.vector_store import (
    get_vector_store
)

from observability.phoenix_config import (
    tracer
)

from opentelemetry.trace import (
    get_current_span
)


# =============================================================================
# VECTOR STORE INSTANCE
# =============================================================================

def get_vector_store_instance():

    return get_vector_store()


# =============================================================================
# DOCUMENT RETRIEVAL
# =============================================================================

@tracer.chain
def retrieve_documents(

    query,

    filters=None,

    k=2
):

    # =========================================================================
    # ACTIVE SPAN
    # =========================================================================

    span = get_current_span()

    # =========================================================================
    # QUERY METRICS
    # =========================================================================

    span.set_attribute(

        "retrieval.query",

        query[:500]
    )

    span.set_attribute(

        "retrieval.query_length",

        len(query)
    )

    span.set_attribute(

        "retrieval.k",

        k
    )

    span.set_attribute(

        "retrieval.has_filters",

        bool(filters)
    )

    if filters:

        span.set_attribute(

            "retrieval.filters",

            str(filters)
        )

    # =========================================================================
    # VECTOR STORE
    # =========================================================================

    vectordb = get_vector_store_instance()

    # =========================================================================
    # FILTERED SEARCH
    # =========================================================================

    if filters:

        results = vectordb.similarity_search(

            query=query,

            k=k,

            filter=filters
        )

    # =========================================================================
    # STANDARD SEARCH
    # =========================================================================

    else:

        results = vectordb.similarity_search(

            query=query,

            k=k
        )

    # =========================================================================
    # RESULT METRICS
    # =========================================================================

    span.set_attribute(

        "retrieval.document_count",

        len(results)
    )

    # =========================================================================
    # DOCUMENT SOURCES
    # =========================================================================

    sources = [

        doc.metadata.get(
            "source",
            "unknown"
        )

        for doc in results
    ]

    span.set_attribute(

        "retrieval.sources",

        str(sources)
    )

    # =========================================================================
    # DOCUMENT CATEGORIES
    # =========================================================================

    categories = [

        doc.metadata.get(
            "category",
            "unknown"
        )

        for doc in results
    ]

    span.set_attribute(

        "retrieval.categories",

        str(categories)
    )

    # =========================================================================
    # RESPONSE SIZE
    # =========================================================================

    total_characters = sum(

        len(doc.page_content)

        for doc in results
    )

    span.set_attribute(

        "retrieval.total_characters",

        total_characters
    )

    # =========================================================================
    # TOP DOCUMENT PREVIEW
    # =========================================================================

    if len(results) > 0:

        span.set_attribute(

            "retrieval.top_document_preview",

            results[0].page_content[:300]
        )

    # =========================================================================
    # AVG DOCUMENT SIZE
    # =========================================================================

    if len(results) > 0:

        average_doc_size = int(

            total_characters / len(results)
        )

        span.set_attribute(

            "retrieval.average_document_size",

            average_doc_size
        )

    # =========================================================================
    # RETRIEVAL SUCCESS
    # =========================================================================

    span.set_attribute(

        "retrieval.success",

        len(results) > 0
    )

    return results