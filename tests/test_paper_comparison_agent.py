from app.pipeline.paper_comparison_agent import compare_papers


def main():

    comparison_input = {
        "paper_count": 2,

        "papers": [
            {
                "paper_index": 1,
                "topic": "Retrieval Augmented Generation",

                "main_findings": [
                    {
                        "text": "RAG improves knowledge-intensive tasks.",
                        "evidence": "RAG enhances accuracy..."
                    }
                ],

                "methods": [
                    {
                        "text": "Uses retrieval and generation.",
                        "evidence": "retrieval and generation..."
                    }
                ],

                "results": [],
                "limitations": [],
                "research_gaps": [],
            },

            {
                "paper_index": 2,
                "topic": "Retrieval Augmented Generation",

                "main_findings": [
                    {
                        "text": "RAG reduces hallucination.",
                        "evidence": "RAG reduces factually incorrect content..."
                    }
                ],

                "methods": [
                    {
                        "text": "Uses retrieval with reranking.",
                        "evidence": "reranking improves retrieval..."
                    }
                ],

                "results": [],
                "limitations": [],
                "research_gaps": [],
            },
        ],
    }

    print("\n================================")
    print("   PAPER COMPARISON AGENT TEST")
    print("================================")

    result = compare_papers(
        topic="Retrieval Augmented Generation",
        comparison_input=comparison_input,
    )

    print("\n--- COMPARISON RESULT ---")

    print(
        f"\nAgreements: "
        f"{len(result.get('agreements', []))}"
    )

    print(
        f"Differences: "
        f"{len(result.get('differences', []))}"
    )

    print(
        f"Contradictions: "
        f"{len(result.get('contradictions', []))}"
    )

    print(
        f"Method comparisons: "
        f"{len(result.get('method_comparisons', []))}"
    )

    print(
        f"Result comparisons: "
        f"{len(result.get('result_comparisons', []))}"
    )

    print(
        f"Research gaps: "
        f"{len(result.get('research_gaps', []))}"
    )

    print(
        "\n✓ Paper comparison completed"
    )


if __name__ == "__main__":
    main()