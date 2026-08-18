from app.pipeline.research_search_pipeline import run_search_pipeline


def main():

    result = run_search_pipeline(
        topic="Retrieval Augmented Generation",
        max_chunks=3,
    )

    print("\n\n================================")
    print("      FINAL RESEARCH STATE")
    print("================================")

    print(
        f"\nTopic: {result['topic']}"
    )

    print(
        f"Paper: "
        f"{result['search']['selected_paper']['title']}"
    )

    print(
        f"Year: "
        f"{result['search']['selected_paper'].get('publication_year')}"
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

    print("\n✓ COMPLETE END-TO-END RESEARCH FLOW")


if __name__ == "__main__":
    main()