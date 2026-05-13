import json
from pathlib import Path

from langchain_core.documents import Document

from app.rag.chunker import get_text_splitter
from app.rag.vector_store import get_vector_store

from app.observability.traces import logger

MARKDOWN_DIR = "app/docs/pension_markdowns"


def extract_metadata(text):

    metadata = {}

    lines = text.splitlines()

    json_start = None
    json_end = None

    for i, line in enumerate(lines):

        if "```json" in line:
            json_start = i + 1
            continue

        if json_start is not None and "```" in line:
            json_end = i
            break

    if json_start is not None and json_end is not None:

        try:
            json_text = "\n".join(lines[json_start:json_end]).strip()

            metadata = json.loads(json_text)

        except Exception as e:
            logger.warning(f"Metadata extraction failed: {e}")

    return metadata


def load_markdown_documents():

    docs = []

    for file_path in Path(MARKDOWN_DIR).glob("*.md"):

        logger.info(f"Loading file: {file_path.name}")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        metadata = extract_metadata(text)

        metadata["source"] = file_path.name

        docs.append(
            Document(
                page_content=text,
                metadata=metadata
            )
        )

        logger.info(f"Metadata extracted: {metadata}")

    return docs


def ingest_documents():

    logger.info("Starting document ingestion")

    documents = load_markdown_documents()

    splitter = get_text_splitter()

    chunks = splitter.split_documents(documents)

    logger.info(f"Generated {len(chunks)} chunks")

    vectordb = get_vector_store()

    vectordb.add_documents(chunks)

    logger.info("Ingestion completed successfully")

    print(f"Ingested {len(chunks)} chunks successfully.")


if __name__ == "__main__":
    ingest_documents()