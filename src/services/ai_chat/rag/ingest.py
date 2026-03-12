from src.services.ai_chat.rag.embeddings import generate_embedding
from src.services.ai_chat.rag.vector_store import insert_document


def ingest_documents(documents: list[str]):
    """
    Ingest documents into Supabase vector DB
    """

    for doc in documents:

        embedding = generate_embedding(doc)

        insert_document(
            content=doc,
            embedding=embedding
        )

    print("Documents ingested successfully.")

documents = [
    "Tomato early blight causes brown circular spots on leaves.",
    "Powdery mildew appears as white powder on plant leaves.",
    "Aphids damage plants by sucking sap from leaves.",
    "Nitrogen fertilizer improves plant leaf growth."
]

ingest_documents(documents)