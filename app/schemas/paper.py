from dataclasses import dataclass, field


@dataclass
class Paper:
    """
    Metadata describing an academic paper.
    """

    title: str

    authors: list[str] = field(default_factory=list)

    year: int | None = None

    doi: str | None = None

    url: str | None = None

    pdf_url: str | None = None