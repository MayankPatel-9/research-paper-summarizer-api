import fitz


def extract_text(file_path: str) -> dict[str, str]:
    """Extract a title and full text from a PDF file."""
    with fitz.open(file_path) as pdf:
        metadata_title = (pdf.metadata or {}).get("title", "").strip()
        page_text = [page.get_text() for page in pdf]

    full_text = "\n".join(page_text).strip()
    title = metadata_title or _first_non_empty_line(full_text)

    return {
        "title": title,
        "full_text": full_text,
    }


def _first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line

    return ""
