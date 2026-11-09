from pathlib import Path

from app.ingestion.document_loader import load_document
from app.ingestion.chunker import chunk_text
from app.ingestion.metadata import (
    generate_document_metadata,
    generate_chunk_records
)


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
    ".csv"
}


def process_document(
    file_path: str,
    chunk_size: int = 100,
    chunk_overlap: int = 20
) -> list[dict]:

    path = Path(file_path)

    print(f"Processing document: {path.name}")

    # Step 1: Extract document content
    text = load_document(file_path)

    if not text.strip():
        raise ValueError("Document contains no extractable text.")

    print(f"Extracted {len(text)} characters.")

    # Step 2: Generate chunks
    chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    print(f"Generated {len(chunks)} chunks.")

    # Step 3: Generate document metadata
    document_metadata = generate_document_metadata(file_path)

    # Step 4: Generate metadata-rich chunk records
    chunk_records = generate_chunk_records(
        chunks,
        document_metadata
    )

    print(f"Generated {len(chunk_records)} structured records.")

    return chunk_records


def process_directory(
    directory_path: str,
    chunk_size: int = 100,
    chunk_overlap: int = 20
) -> dict[str, list[dict]]:

    directory = Path(directory_path)

    if not directory.exists():
        raise FileNotFoundError(
            f"Directory not found: {directory_path}"
        )

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Not a directory: {directory_path}"
        )

    processed_documents = {}

    files = sorted(
        file for file in directory.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    for file_path in files:

        try:
            records = process_document(
                str(file_path),
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )

            processed_documents[file_path.name] = records

        except Exception as error:
            print(f"Failed to process {file_path.name}: {error}")

    return processed_documents


if __name__ == "__main__":

    results = process_directory(
        "data/raw/",
        chunk_size=30,
        chunk_overlap=5
    )

    print("\n========== BATCH PROCESSING SUMMARY ==========")

    total_chunks = 0

    for filename, records in results.items():

        print(f"\nDocument: {filename}")

        for record in records:

            print("\n-----------------------------")

            print(f"Document ID: {record['document_id']}")
            print(f"Chunk ID: {record['chunk_id']}")
            print(f"Chunk Index: {record['chunk_index']}")
            print(f"Content: {record['content']}")

        total_chunks += len(records)

        print(f"\nTotal chunks: {len(records)}")

    print("\n========== FINAL SUMMARY ==========")
    print(f"Total documents processed: {len(results)}")
    print(f"Total chunks generated: {total_chunks}")
