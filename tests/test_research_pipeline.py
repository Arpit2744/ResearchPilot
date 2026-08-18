from app.pipeline.research_pipeline import run_research_pipeline


TOPIC = "Retrieval Augmented Generation"

PAPER_URL = (
    "https://arxiv.org/pdf/2312.10997"
)


def main():

    result = run_research_pipeline(
        topic=TOPIC,
        paper_url=PAPER_URL,

        # IMPORTANT:
        # We deliberately analyze only 3 chunks
        # for the first end-to-end test.
        max_chunks=3,
    )

    print("\n\n--- FINAL RESEARCH STATE ---")

    print(
        f"Topic: {result['topic']}"
    )

    print(
        f"Pages: "
        f"{result['paper']['page_count']}"
    )

    print(
        f"Total chunks: "
        f"{result['chunks']['total']}"
    )

    print(
        f"Analyzed chunks: "
        f"{result['chunks']['analyzed']}"
    )

    print("\nPipeline successfully completed.")


if __name__ == "__main__":
    main()