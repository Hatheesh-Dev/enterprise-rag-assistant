from pathlib import Path
import csv
import pymupdf
from docx import Document


def load_txt(file_path: Path) -> str:
    """Extract text from TXT and Markdown files."""
    return file_path.read_text(encoding="utf-8")


def load_pdf(file_path: Path) -> str:
    """Extract text from a PDF file."""
    text = []

    with pymupdf.open(file_path) as pdf:
        for page in pdf:
            text.append(page.get_text())

    return "\n".join(text)


def load_docx(file_path: Path) -> str:
    """Extract text from a Word document."""
    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def load_csv(file_path: Path) -> str:
    """Extract text from a CSV file."""
    rows = []

    with open(file_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            rows.append(" | ".join(row))

    return "\n".join(rows)


def load_document(file_path: str) -> str:
    """
    Load a document based on its file extension.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    extension = path.suffix.lower()

    if extension in [".txt", ".md"]:
        return load_txt(path)

    elif extension == ".pdf":
        return load_pdf(path)

    elif extension == ".docx":
        return load_docx(path)

    elif extension == ".csv":
        return load_csv(path)

    else:
        raise ValueError(f"Unsupported file format: {extension}")


if __name__ == "__main__":

    document_path = "data/raw/network_troubleshooting.txt"

    content = load_document(document_path)

    print("Document loaded successfully!")
    print("--------------------------------")
    print(content)
