import io
import httpx

from pypdf import PdfReader


def read_paper(url: str) -> dict:
    """
    Download a PDF and extract text while preserving page boundaries.
    """

    response = httpx.get(
        url,
        timeout=30.0,
        follow_redirects=True,
        headers={
            "User-Agent": "ResearchPilot/0.1"
        },
    )

    response.raise_for_status()

    content_type = response.headers.get("content-type", "")

    if "pdf" not in content_type.lower() and not url.lower().endswith(".pdf"):
        raise ValueError(
            f"Expected a PDF but received: {content_type}"
        )

    reader = PdfReader(io.BytesIO(response.content))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            {
                "page": page_number,
                "text": text,
            }
        )

    full_text = "\n\n".join(
        page["text"] for page in pages
    )

    return {
        "url": url,
        "page_count": len(pages),
        "pages": pages,
        "text": full_text,
    }