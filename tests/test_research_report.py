from app.pipeline.research_report import build_research_report


def main():

    synthesis = {
        "main_findings": [
            {
                "text": "RAG improves knowledge-intensive generation.",
                "evidence": "RAG enhances the accuracy..."
            }
        ],

        "problems": [
            {
                "text": "LLMs can hallucinate.",
                "evidence": "LLMs encounter challenges like hallucination..."
            }
        ],

        "methods": [],
        "datasets": [],
        "metrics": [],
        "results": [],
        "limitations": [],
        "technical_concepts": [],
        "evidence": [],
        "research_gaps": [
            {
                "text": "Lack of systematic synthesis.",
                "evidence": "not been accompanied by a systematic synthesis..."
            }
        ],
    }

    report = build_research_report(
        topic="Retrieval Augmented Generation",
        synthesis=synthesis,
    )

    print("\n================================")
    print("      RESEARCH REPORT TEST")
    print("================================")

    print(f"\nTitle: {report['title']}")

    print(
        f"\nMain findings: "
        f"{len(report['executive_summary']['main_findings'])}"
    )

    print(
        f"Problems: "
        f"{len(report['executive_summary']['problems'])}"
    )

    print(
        f"Research gaps: "
        f"{len(report['research_gaps'])}"
    )

    print("\n✓ Research report created successfully")


if __name__ == "__main__":
    main()