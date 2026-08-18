import json
import os
from dataclasses import asdict

from dotenv import load_dotenv
from google import genai
from mistralai.client import Mistral


load_dotenv()


# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY not found in .env"
    )

if not MISTRAL_API_KEY:
    raise RuntimeError(
        "MISTRAL_API_KEY not found in .env"
    )


gemini_client = genai.Client(
    api_key=GOOGLE_API_KEY
)

mistral_client = Mistral(
    api_key=MISTRAL_API_KEY
)


GEMINI_MODEL = "gemini-3.6-flash"

MISTRAL_MODEL = "mistral-small-latest"


# --------------------------------------------------
# SYSTEM INSTRUCTION
# --------------------------------------------------

SYSTEM_INSTRUCTION = """
You are a research comparison agent.

You will receive structured research syntheses
from multiple academic papers.

Compare ONLY the information provided.

Do NOT introduce outside knowledge.

Do NOT invent claims, results, methods,
datasets, metrics, limitations, or research gaps.

Identify:

- agreements between papers
- differences between papers
- contradictions between papers
- methodological differences
- result differences
- shared limitations
- paper-specific limitations
- research gaps explicitly supported by the papers

IMPORTANT:

A difference is NOT automatically a contradiction.

Only classify something as a contradiction when
the provided evidence supports opposing claims.

Every important comparison should preserve
the supporting paper index and evidence.

Return ONLY valid JSON.
"""


# --------------------------------------------------
# JSON HELPERS
# --------------------------------------------------

def _clean_json(text: str) -> str:
    """
    Remove accidental markdown code fences.
    """

    text = text.strip()

    if text.startswith("```"):
        text = text.replace(
            "```json",
            "",
            1,
        )

        text = text.replace(
            "```",
            "",
        )

        text = text.strip()

    return text


# --------------------------------------------------
# COMPARISON
# --------------------------------------------------

def compare_papers(
    topic: str,
    comparison_input: dict,
) -> dict:
    """
    Compare multiple paper syntheses.

    Gemini is attempted first.
    Mistral is used as fallback.
    """

    if not comparison_input:
        raise ValueError(
            "Comparison input cannot be empty."
        )

    prompt = f"""
{SYSTEM_INSTRUCTION}

Research topic:
{topic}

Number of papers:
{comparison_input.get("paper_count", 0)}

Paper syntheses:
----------------

{json.dumps(
    comparison_input,
    indent=2,
    ensure_ascii=False,
)}

----------------

Return JSON using exactly this structure:

{{
  "topic": "{topic}",

  "agreements": [],

  "differences": [],

  "contradictions": [],

  "method_comparisons": [],

  "result_comparisons": [],

  "shared_limitations": [],

  "paper_specific_limitations": [],

  "research_gaps": []
}}

Each comparison item should preferably use:

{{
  "text": "...",
  "papers": [1, 2],
  "evidence": [
    {{
      "paper": 1,
      "text": "..."
    }},
    {{
      "paper": 2,
      "text": "..."
    }}
  ]
}}

For paper-specific findings:

{{
  "text": "...",
  "papers": [1],
  "evidence": [
    {{
      "paper": 1,
      "text": "..."
    }}
  ]
}}

Only include research gaps explicitly
supported by the provided paper syntheses.

Do not infer a research gap merely because
the papers failed to mention something.
"""

    # --------------------------------------------------
    # GEMINI
    # --------------------------------------------------

    try:

        print(
            "      → Trying Gemini for comparison..."
        )

        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        text = _clean_json(
            response.text
        )

        result = json.loads(text)

        print(
            "      ✓ Gemini comparison succeeded"
        )

        return result

    except Exception as exc:

        print(
            f"      ⚠ Gemini comparison failed: "
            f"{type(exc).__name__}"
        )

    # --------------------------------------------------
    # MISTRAL FALLBACK
    # --------------------------------------------------

    try:

        print(
            "      → Falling back to Mistral..."
        )

        response = mistral_client.chat.complete(
            model=MISTRAL_MODEL,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        text = _clean_json(
            response.choices[0].message.content
        )

        result = json.loads(text)

        print(
            "      ✓ Mistral comparison succeeded"
        )

        return result

    except Exception as exc:

        raise RuntimeError(
            "Both Gemini and Mistral failed "
            "during paper comparison."
        ) from exc