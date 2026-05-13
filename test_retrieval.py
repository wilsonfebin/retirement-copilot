from app.rag.retriever import retrieve_documents


query = "Which pension plans provide guaranteed income?"

filters = {
    "guaranteed_income": True
}

results = retrieve_documents(
    query=query,
    filters=filters
)

for i, doc in enumerate(results):

    print("\n")
    print("=" * 80)
    print(f"Result {i + 1}")

    print("\nMETADATA:")
    print(doc.metadata)

    print("\nCONTENT:")
    print(doc.page_content[:1200])