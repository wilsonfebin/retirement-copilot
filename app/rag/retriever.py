from app.rag.vector_store import get_vector_store


def get_vector_store_instance():

    return get_vector_store()


def retrieve_documents(query, filters=None, k=4):

    vectordb = get_vector_store_instance()

    results = vectordb.max_marginal_relevance_search(
        query=query,
        k=k,
        fetch_k=10,
        filter=filters
    )

    return results