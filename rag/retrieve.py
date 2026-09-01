import requests
import chromadb

OLLAMA_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text"


def create_query_embedding(question):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": [question]
        }
    )

    response.raise_for_status()

    return response.json()["embeddings"][0]


def retrieve_plans(question, number_of_results=3):
    client = chromadb.PersistentClient(
        path="data/chroma"
    )

    collection = client.get_collection(
        name="production_plans"
    )

    query_embedding = create_query_embedding(
        question
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=number_of_results
    )

    return results


if __name__ == "__main__":
    question = input(
        "Ask about the production plans: "
    )

    results = retrieve_plans(
        question
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    for i, document in enumerate(documents):
        print("\n--- Retrieved Plan ---")
        print(f"Distance: {distances[i]}")
        print(document)