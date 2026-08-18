import httpx

OPENALEX_URL = "https://api.openalex.org/works"


def resolve_pdf_url(url: str | None) -> str | None:
    """
    Convert known academic landing-page URLs into PDF URLs.
    """

    if not url:
        return None

    # arXiv abstract page
    if "arxiv.org/abs/" in url:
        paper_id = url.split("arxiv.org/abs/", 1)[1]
        return f"https://arxiv.org/pdf/{paper_id}"

    return url


def search_papers(query: str, max_results: int = 5) -> dict:
    """Search OpenAlex for academic papers matching a research query."""

    params = {
        "search": query,
        "per-page": max_results,
        "select": (
            "id,title,publication_year,doi,"
            "authorships,primary_location"
        ),
    }

    response = httpx.get(
        OPENALEX_URL,
        params=params,
        timeout=20.0,
    )

    response.raise_for_status()

    data = response.json()

    papers = []

    for work in data.get("results", []):
        authors = []

        for authorship in work.get("authorships", []):
            author = authorship.get("author")

            if author and author.get("display_name"):
                authors.append(author["display_name"])

        primary_location = work.get("primary_location") or {}

        landing_url = primary_location.get("landing_page_url")
        openalex_pdf_url = primary_location.get("pdf_url")

        # Prefer OpenAlex's known PDF URL.
        # If unavailable, try resolving the landing page ourselves.
        pdf_url = (
            openalex_pdf_url
            or resolve_pdf_url(landing_url)
        )

        papers.append(
            {
                "title": work.get("title"),
                "authors": authors,
                "year": work.get("publication_year"),
                "doi": work.get("doi"),
                "url": landing_url,
                "pdf_url": pdf_url,
            }
        )

    return {
        "query": query,
        "count": len(papers),
        "papers": papers,
    }