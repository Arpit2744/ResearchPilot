from app.pipeline.paper_reader import read_paper
from app.pipeline.paper_chunker import split_into_chunks
from app.pipeline.chunk_analyzer import analyze_chunk
from app.pipeline.synthesizer import synthesize_analyses


PDF_URL = "https://arxiv.org/pdf/2312.10997"


def main():

    print("\n--- Reading Paper ---")

    paper = read_paper(PDF_URL)

    print(
        f"Pages: {paper['page_count']}"
    )

    print("\n--- Chunking Paper ---")

    chunks = split_into_chunks(
        paper["pages"],
        max_chars=12000,
        overlap=1000,
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    print("\n--- Analyzing Chunks ---")

    analyses = []

    # Keep this at 3 for now.
    for chunk in chunks[:3]:

        print(
            f"Analyzing {chunk.chunk_id} "
            f"(pages {chunk.start_page}-{chunk.end_page})"
        )

        analysis = analyze_chunk(chunk)

        analyses.append(analysis)

        print("✓ complete")

    print("\n--- Synthesizing ---")

    result = synthesize_analyses(
        topic="Retrieval Augmented Generation",
        analyses=analyses,
    )

    print("\n--- SYNTHESIS RESULT ---")

    print(result)

    print("\n--- Synthesizer Test Finished ---")


if __name__ == "__main__":
    main()