from app.rag.vector_store import get_vector_store


def get_vector_store_instance():

    return get_vector_store()


def retrieve_documents(query, filters=None, k=2):

    vectordb = get_vector_store_instance()

    if filters:

        results = vectordb.similarity_search(
            query=query,
            k=k,
            filter=filters
        )

    else:

        results = vectordb.similarity_search(
            query=query,
            k=k,
        )

    return results