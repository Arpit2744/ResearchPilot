from .paper_search import search_papers
from .research_pipeline import run_research_pipeline


def run_search_pipeline(
    topic: str,
    max_results: int = 5,
    max_chunks: int = 3,
):
    """
    ResearchPilot vertical slice:

    Topic
      ↓
    OpenAlex paper search
      ↓
    Select best paper
      ↓
    Read paper
      ↓
    Chunk
      ↓
    Analyze
    """

    print("\n================================")
    print("   RESEARCHPILOT SEARCH PIPELINE")
    print("================================")

    print(f"\nResearch topic: {topic}")

    # --------------------------------------------------
    # 1. SEARCH
    # --------------------------------------------------

    print("\n[1/4] Searching papers...")

    search_result = search_papers(
        query=topic,
        max_results=max_results,
    )

    papers = search_result["papers"]

    if not papers:
        raise RuntimeError(
            f"No papers found for topic: {topic}"
        )

    print(
        f"      ✓ {len(papers)} papers found"
    )

    # --------------------------------------------------
    # 2. SELECT
    # --------------------------------------------------

    print("\n[2/4] Selecting paper...")

    selected = papers[0]

    print(
        f"      ✓ {selected['title']}"
    )

    print(
        f"      Year: {selected.get('year')}"
    )

    print(
        f"      URL: {selected.get('url')}"
    )

    # --------------------------------------------------
    # 3 + 4. READ → CHUNK → ANALYZE
    # --------------------------------------------------

    print("\n[3/4] Running research pipeline...")

    result = run_research_pipeline(
        topic=topic,
        paper_url=selected["pdf_url"],
        max_chunks=max_chunks,
    )

    # --------------------------------------------------
    # ADD SEARCH INFORMATION
    # --------------------------------------------------

    result["search"] = {
        "query": topic,
        "papers_found": search_result["count"],
        "selected_paper": selected,
    }

    print("\n[4/4] Search pipeline complete.")

    return result