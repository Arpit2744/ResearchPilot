from dataclasses import dataclass


@dataclass
class EvidenceItem:
    """
    A research finding extracted from a paper chunk.
    """

    text: str
    evidence: str = ""

@dataclass
class ChunkAnalysis:
    """
    Structured research information extracted from one paper chunk.
    """

    chunk_id: str

    start_page: int
    end_page: int

    claims: list[EvidenceItem]
    problems: list[EvidenceItem]
    methods: list[EvidenceItem]
    datasets: list[EvidenceItem]
    metrics: list[EvidenceItem]
    results: list[EvidenceItem]
    limitations: list[EvidenceItem]
    technical_concepts: list[EvidenceItem]
    evidence: list[EvidenceItem]

