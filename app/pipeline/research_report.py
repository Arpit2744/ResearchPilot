from datetime import datetime


def build_research_report(
    topic: str,
    synthesis: dict,
) -> dict:
    """
    Convert structured research synthesis into a user-facing
    research report.

    This layer does not generate new research information.
    It only organizes the synthesis into a report structure.
    """

    if not synthesis:
        raise ValueError(
            "Cannot build research report without synthesis."
        )

    report = {
        "title": f"Research Report: {topic}",

        "topic": topic,

        "generated_at": datetime.now().isoformat(),

        "executive_summary": {
            "main_findings": synthesis.get(
                "main_findings", []
            ),

            "problems": synthesis.get(
                "problems", []
            ),

            "results": synthesis.get(
                "results", []
            ),
        },

        "research_findings": {
            "methods": synthesis.get(
                "methods", []
            ),

            "datasets": synthesis.get(
                "datasets", []
            ),

            "metrics": synthesis.get(
                "metrics", []
            ),

            "results": synthesis.get(
                "results", []
            ),
        },

        "limitations": synthesis.get(
            "limitations", []
        ),

        "technical_concepts": synthesis.get(
            "technical_concepts", []
        ),

        "research_gaps": synthesis.get(
            "research_gaps", []
        ),

        "evidence": synthesis.get(
            "evidence", []
        ),
    }

    return report