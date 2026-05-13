from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def get_embeddings():

    return OpenAIEmbeddings(
        model="text-embedding-3-small"
    )