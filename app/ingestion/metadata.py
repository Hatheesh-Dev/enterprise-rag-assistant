from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4


def generate_document_metadata(file_path: str) -> dict:
    """
    Generate metadata for a source document.
    """

    path = Path(file_path)

    return {
        "document_id": str(uuid4()),
        "document_name": path.name,
        "file_type": path.suffix.lower().replace(".", ""),
        "created_at": datetime.now(timezone.utc).isoformat()
    }


def generate_chunk_records(
    chunks: list[str],
    document_metadata: dict
) -> list[dict]:
    """
    Generate metadata-rich records for document chunks.
    """

    chunk_records = []

    for index, chunk in enumerate(chunks, start=1):

        record = {
            **document_metadata,
            "chunk_id": f"{document_metadata['document_id']}_chunk_{index}",
            "chunk_index": index,
            "content": chunk
        }

        chunk_records.append(record)

    return chunk_records


if __name__ == "__main__":

    sample_file = "data/raw/network_troubleshooting.txt"

    metadata = generate_document_metadata(sample_file)

    sample_chunks = [
        "Employees should check physical network connections.",
        "Verify DNS resolution using nslookup."
    ]

    records = generate_chunk_records(
        sample_chunks,
        metadata
    )

    for record in records:
        print("\n-----------------------------")
        for key, value in record.items():
            print(f"{key}: {value}")
