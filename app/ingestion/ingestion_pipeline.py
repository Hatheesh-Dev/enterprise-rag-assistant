from pathlib import Path

from app.ingestion.document_loader import load_document
from app.ingestion.chunker import chunk_text


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
) -> list[str]:

    path = Path(file_path)

    print(f"Processing document: {path.name}")

    text = load_document(file_path)

    if not text.strip():
        raise ValueError("Document contains no extractable text.")

    chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    print(f"Extracted {len(text)} characters.")
    print(f"Generated {len(chunks)} chunks.")

    return chunks


def process_directory(
    directory_path: str,
    chunk_size: int = 100,
    chunk_overlap: int = 20
) -> dict[str, list[str]]:

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
            chunks = process_document(
                str(file_path),
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )

            processed_documents[file_path.name] = chunks

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

    for filename, chunks in results.items():

        print(f"\nDocument: {filename}")
        print(f"Chunks: {len(chunks)}")

        total_chunks += len(chunks)

    print(f"\nTotal documents processed: {len(results)}")
    print(f"Total chunks generated: {total_chunks}")
