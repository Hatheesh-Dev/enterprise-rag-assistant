from pathlib import Path

from app.ingestion.document_loader import load_document
from app.ingestion.chunker import chunk_text


def process_document(
    file_path: str,
    chunk_size: int = 100,
    chunk_overlap: int = 20
) -> list[str]:
    """
    Load a document and split its content into chunks.
    """

    path = Path(file_path)

    print(f"Processing document: {path.name}")

    # Step 1: Extract document content
    text = load_document(file_path)

    if not text.strip():
        raise ValueError("Document contains no extractable text.")

    print(f"Extracted {len(text)} characters.")

    # Step 2: Split extracted text into chunks
    chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    print(f"Generated {len(chunks)} chunks.")

    return chunks


if __name__ == "__main__":

    document_path = "data/raw/network_troubleshooting.txt"

    document_chunks = process_document(
        document_path,
        chunk_size=30,
        chunk_overlap=5
    )

    for index, chunk in enumerate(document_chunks, start=1):

        print(f"\n--- Chunk {index} ---")
        print(chunk)
        print(f"Word count: {len(chunk.split())}")
