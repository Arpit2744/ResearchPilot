from .paper_reader import read_paper
from .paper_chunker import split_into_chunks
from .chunk_analyzer import analyze_chunk
from .synthesizer import synthesize_analyses

def run_research_pipeline(
    topic: str,
    paper_url: str,
    max_chunks: int = 3,
):
    """
    Minimal end-to-end ResearchPilot pipeline.

    Topic
      ↓
    Read paper
      ↓
    Chunk paper
      ↓
    Analyze chunks
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

    print("\n[1/3] Reading paper...")

    paper = read_paper(paper_url)

    print(
        f"      ✓ {paper['page_count']} pages extracted"
    )

    # --------------------------------------------------
    # 2. CHUNK
    # --------------------------------------------------

    print("\n[2/3] Creating chunks...")

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

    print("\n[3/3] Analyzing chunks...")

    analyses = []

    chunks_to_process = chunks[:max_chunks]

    for index, chunk in enumerate(chunks_to_process, start=1):

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

    print("\n[4/4] Synthesizing research findings...")

    synthesis = synthesize_analyses(
        topic=topic,
        analyses=analyses,
    )

    print("      ✓ synthesis complete")
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
    }

    print("\n================================")
    print("      RESEARCHPIPELINE DONE")
    print("================================")

    return research_state