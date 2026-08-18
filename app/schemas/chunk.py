from dataclasses import dataclass


@dataclass
class PaperChunk:
    """
    A page-aware chunk of a research paper.
    """

    chunk_id: str
    text: str

    start_page: int
    end_page: int

    section: str = "Unclassified"
    section_confidence: float = 0.0