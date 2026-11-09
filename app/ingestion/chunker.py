def chunk_text(
    text: str,
    chunk_size: int = 100,
    chunk_overlap: int = 20
) -> list[str]:
    """
    Split text into word-based chunks with overlapping words.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("Chunk overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be smaller than chunk size."
        )

    words = text.split()

    chunks = []
    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)

        chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


if __name__ == "__main__":

    sample_text = """
    Employees experiencing network connectivity issues should first
    check their physical network connections.

    If websites are not accessible, verify DNS resolution using
    the nslookup command.

    Employees working remotely should verify their VPN connection
    before escalating network-related issues.
    """

    chunks = chunk_text(
        sample_text,
        chunk_size=20,
        chunk_overlap=5
    )

    for index, chunk in enumerate(chunks, start=1):

        print(f"\n--- Chunk {index} ---")
        print(chunk)
        print(f"Word count: {len(chunk.split())}")
