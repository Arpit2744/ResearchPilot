from .paper_reader import read_paper
from .paper_chunker import split_into_chunks
from .chunk_analyzer import analyze_chunk
from .synthesizer import synthesize_analyses
from .research_report import build_research_report


def run_research_pipeline(
    topic: str,
    paper_url: str,
    max_chunks: int = 3,
):
    """
    End-to-end ResearchPilot research pipeline.

    Topic
      ↓
    Read paper
      ↓
    Chunk paper
      ↓
    Analyze chunks
      ↓
    Synthesize findings
      ↓
    Build research report
      ↓
    Return research state
    """

    print("\n================================")
    print("       RESEARCHPILOT MVP")
    print("================================")

    print(f"\nResearch topic: {topic}")

    # --------------------------------------------------
    # 1. READ
    # --------------------------------------------------

    print("\n[1/5] Reading paper...")

    paper = read_paper(paper_url)

    print(
        f"      ✓ {paper['page_count']} pages extracted"
    )

    # --------------------------------------------------
    # 2. CHUNK
    # --------------------------------------------------

    print("\n[2/5] Creating chunks...")

    chunks = split_into_chunks(
        paper["pages"],
        max_chars=12000,
        overlap=1000,
    )

    print(
        f"      ✓ {len(chunks)} chunks created"
    )

    # --------------------------------------------------
    # 3. ANALYZE
    # --------------------------------------------------

    print("\n[3/5] Analyzing chunks...")

    analyses = []

    chunks_to_process = chunks[:max_chunks]

    for index, chunk in enumerate(
        chunks_to_process,
        start=1,
    ):

        print(
            f"      → Analyzing chunk "
            f"{index}/{len(chunks_to_process)} "
            f"(pages {chunk.start_page}-{chunk.end_page})"
        )

        result = analyze_chunk(chunk)

        analyses.append(result)

        print("        ✓ complete")

    # --------------------------------------------------
    # 4. SYNTHESIZE
    # --------------------------------------------------

    print("\n[4/5] Synthesizing research findings...")

    synthesis = synthesize_analyses(
        topic=topic,
        analyses=analyses,
    )

    print("      ✓ synthesis complete")

    # --------------------------------------------------
    # 5. REPORT
    # --------------------------------------------------

    print("\n[5/5] Building research report...")

    report = build_research_report(
        topic=topic,
        synthesis=synthesis,
    )

    print("      ✓ research report built")

    # --------------------------------------------------
    # RESEARCH STATE
    # --------------------------------------------------

    research_state = {
        "topic": topic,

        "paper": {
            "url": paper_url,
            "page_count": paper["page_count"],
            "character_count": len(paper["text"]),
        },

        "chunks": {
            "total": len(chunks),
            "analyzed": len(analyses),
        },

        "analyses": analyses,

        "synthesis": synthesis,

        "report": report,
    }

    # --------------------------------------------------
    # DONE
    # --------------------------------------------------

    print("\n================================")
    print("      RESEARCHPIPELINE DONE")
    print("================================")

    return research_state