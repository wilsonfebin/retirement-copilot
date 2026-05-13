from langchain_chroma import Chroma

from app.rag.embeddings import get_embeddings

CHROMA_PATH = "chroma_db"


def get_vector_store():

    embeddings = get_embeddings()

    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )