from pathlib import Path


def load_document(file_path: str) -> str:
    """
    Read a text document and return its content.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    content = path.read_text(encoding="utf-8")

    return content


if __name__ == "__main__":

    document_path = "data/raw/network_troubleshooting.txt"

    document_content = load_document(document_path)

    print("Document loaded successfully!")
    print("--------------------------------")

    print(document_content)
