from typing import List, Dict


def compare_paper_syntheses(
    syntheses: List[Dict],
) -> Dict:
    """
    Prepare structured information for cross-paper comparison.

    This first version does NOT use an LLM.
    It organizes multiple paper syntheses so that
    a later comparison agent can reason over them.
    """

    if not syntheses:
        raise ValueError(
            "Cannot compare papers without syntheses."
        )

    papers = []

    for index, synthesis in enumerate(
        syntheses,
        start=1,
    ):

        papers.append(
            {
                "paper_index": index,
                "topic": synthesis.get(
                    "topic",
                    "",
                ),
                "main_findings": synthesis.get(
                    "main_findings",
                    [],
                ),
                "problems": synthesis.get(
                    "problems",
                    [],
                ),
                "methods": synthesis.get(
                    "methods",
                    [],
                ),
                "datasets": synthesis.get(
                    "datasets",
                    [],
                ),
                "metrics": synthesis.get(
                    "metrics",
                    [],
                ),
                "results": synthesis.get(
                    "results",
                    [],
                ),
                "limitations": synthesis.get(
                    "limitations",
                    [],
                ),
                "technical_concepts": synthesis.get(
                    "technical_concepts",
                    [],
                ),
                "research_gaps": synthesis.get(
                    "research_gaps",
                    [],
                ),
                "evidence": synthesis.get(
                    "evidence",
                    [],
                ),
            }
        )

    return {
        "paper_count": len(papers),
        "papers": papers,
    }