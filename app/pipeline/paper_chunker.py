import re
from ..schemas.chunk import PaperChunk


SECTION_PATTERNS = [
    ("abstract", "Abstract"),
    ("introduction", "Introduction"),
    ("background", "Background"),
    ("related work", "Related Work"),
    ("literature review", "Literature Review"),
    ("methodology", "Methodology"),
    ("method", "Method"),
    ("approach", "Approach"),
    ("materials and methods", "Materials and Methods"),
    ("experiments", "Experiments"),
    ("experimental setup", "Experimental Setup"),
    ("results", "Results"),
    ("discussion", "Discussion"),
    ("limitations", "Limitations"),
    ("conclusion", "Conclusion"),
    ("future work", "Future Work"),
    ("references", "References"),
]


def normalize_text(text: str) -> str:
    """
    Fix common PDF extraction artifacts.
    """

    # Join words broken across lines by PDF extraction.
    text = re.sub(r"-\s*\n\s*", "", text)

    # Normalize repeated whitespace while preserving newlines.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def detect_section(text: str):
    """
    Conservative section detector.

    Returns:
        (section_name, confidence)
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:120]:

        # Remove section numbering.
        candidate = re.sub(
            r"^(?:"
            r"(?:[IVXLC]+|\d+(?:\.\d+)*)"
            r"[\.\)]?\s*"
            r")",
            "",
            line,
            flags=re.IGNORECASE,
        ).strip()

        candidate = candidate.rstrip(":.-–—")

        lowered = candidate.lower()

        for pattern, display_name in SECTION_PATTERNS:

            if lowered == pattern:
                return display_name, 1.0

    return "Unclassified", 0.0

def split_page_into_chunks(
    page_text: str,
    page_number: int,
    max_chars: int,
    overlap: int,
    section: str,
    chunk_counter: int,
) -> tuple[list[PaperChunk], int]:
    """
    Split one page into chunks while retaining page metadata.
    """

    chunks = []

    start = 0

    while start < len(page_text):

        end = min(
            start + max_chars,
            len(page_text),
        )

        chunk_text = page_text[start:end]

        detected_section,section_confidence = detect_section(
            chunk_text
        )

        if section_confidence >0:
            section = detected_section

        chunks.append(
            PaperChunk(
                chunk_id=f"chunk_{chunk_counter:04d}",
                section=section,
                text=chunk_text,
                start_page=page_number,
                end_page=page_number,
                section_confidence=section_confidence,
            )
        )

        chunk_counter += 1

        if end >= len(page_text):
            break

        start = max(
            0,
            end - overlap,
        )

    return chunks, chunk_counter

def split_into_chunks(
    pages: list[dict],
    max_chars: int = 12000,
    overlap: int = 1000,
) -> list[PaperChunk]:
    """
    Combine pages into larger chunks while preserving page provenance.

    The chunker does not attempt to semantically understand the paper.
    Section classification is handled separately.
    """

    chunks = []

    chunk_counter = 1

    current_text = []
    current_pages = []

    current_length = 0

    for page in pages:

        page_number = page["page"]
        page_text = normalize_text(page["text"])

        if not page_text:
            continue

        # If adding this page would exceed the target,
        # finalize the current chunk.
        if (
            current_text
            and current_length + len(page_text) > max_chars
        ):

            chunk_text = "\n\n".join(current_text)

            chunks.append(
                PaperChunk(
                    chunk_id=f"chunk_{chunk_counter:04d}",
                    text=chunk_text,
                    start_page=current_pages[0],
                    end_page=current_pages[-1],
                    section="Unclassified",
                    section_confidence=0.0,
                )
            )

            chunk_counter += 1

            # Keep overlap from the end of the previous chunk.
            overlap_text = chunk_text[-overlap:]

            current_text = [overlap_text]
            current_pages = [current_pages[-1]]
            current_length = len(overlap_text)

        current_text.append(page_text)
        current_pages.append(page_number)
        current_length += len(page_text)

    # Final chunk.
    if current_text:

        chunk_text = "\n\n".join(current_text)

        chunks.append(
            PaperChunk(
                chunk_id=f"chunk_{chunk_counter:04d}",
                text=chunk_text,
                start_page=current_pages[0],
                end_page=current_pages[-1],
                section="Unclassified",
                section_confidence=0.0,
            )
        )

    return chunks