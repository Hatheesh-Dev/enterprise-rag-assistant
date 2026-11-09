import os

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env
load_dotenv()

# Configure embedding model
EMBEDDING_MODEL = "text-embedding-3-small"


def get_embedding(text: str) -> list[float]:
    """
    Convert text into a numerical embedding vector.
    """

    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding


if __name__ == "__main__":

    sample_text = (
        "Employees must use strong passwords "
        "to protect company accounts."
    )

    embedding = get_embedding(sample_text)

    print("Embedding generated successfully!")
    print(f"Vector dimensions: {len(embedding)}")
    print(f"First 10 values: {embedding[:10]}")
