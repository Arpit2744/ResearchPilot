from app.pipeline.paper_comparator import compare_paper_syntheses


def main():

    syntheses = [
        {
            "topic": "Retrieval Augmented Generation",

            "main_findings": [
                {
                    "text": "RAG improves knowledge-intensive tasks.",
                    "evidence": "RAG enhances accuracy..."
                }
            ],

            "problems": [],
            "methods": [],
            "datasets": [],
            "metrics": [],
            "results": [],
            "limitations": [],
            "technical_concepts": [],
            "research_gaps": [],
            "evidence": [],
        },

        {
            "topic": "Retrieval Augmented Generation",

            "main_findings": [
                {
                    "text": "RAG can reduce hallucination.",
                    "evidence": "RAG reduces factually incorrect content..."
                }
            ],

            "problems": [],
            "methods": [],
            "datasets": [],
            "metrics": [],
            "results": [],
            "limitations": [],
            "technical_concepts": [],
            "research_gaps": [],
            "evidence": [],
        },
    ]

    comparison = compare_paper_syntheses(
        syntheses
    )

    print("\n================================")
    print("      PAPER COMPARATOR TEST")
    print("================================")

    print(
        f"\nPaper count: "
        f"{comparison['paper_count']}"
    )

    for paper in comparison["papers"]:

        print(
            f"\nPaper {paper['paper_index']}"
        )

        print(
            f"Topic: "
            f"{paper['topic']}"
        )

        print(
            f"Main findings: "
            f"{len(paper['main_findings'])}"
        )

    print(
        "\n✓ Paper comparison input "
        "created successfully"
    )


if __name__ == "__main__":
    main()