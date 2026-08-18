import json
import os
from dataclasses import asdict

from dotenv import load_dotenv
from google import genai


load_dotenv()


API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in .env")


client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"


SYSTEM_INSTRUCTION = """
You are a research synthesis agent.

You will receive structured information extracted from one or more
chunks of an academic paper.

Your job is to synthesize the extracted information into a coherent
research summary.

IMPORTANT RULES:

1. Use ONLY the information provided in the chunk analyses.
2. Do NOT introduce outside knowledge.
3. Do NOT invent claims, results, datasets, metrics, or methods.
4. Preserve uncertainty when the evidence is incomplete.
5. Merge duplicate findings where appropriate.
6. Do not treat an extracted claim as stronger than its supporting evidence.
7. Every important finding should retain supporting evidence and page information.
8. If a category has insufficient information, return an empty list.
9. Distinguish between:
   - what the paper claims
   - problems it addresses
   - methods it describes
   - results it reports
   - limitations it acknowledges
10. Return ONLY valid JSON.
"""


def _serialize_analyses(analyses) -> list[dict]:
    """
    Convert ChunkAnalysis dataclasses into JSON-compatible dictionaries.
    """

    return [
        asdict(analysis)
        for analysis in analyses
    ]


def synthesize_analyses(
    topic: str,
    analyses: list,
) -> dict:
    """
    Synthesize multiple ChunkAnalysis objects into a research-level summary.

    The synthesizer only sees information extracted from the paper chunks.
    It does not retrieve external information.
    """

    if not analyses:
        raise ValueError(
            "Cannot synthesize research without chunk analyses."
        )

    serialized = _serialize_analyses(analyses)

    prompt = f"""
{SYSTEM_INSTRUCTION}

Research topic:
{topic}

Number of analyzed chunks:
{len(analyses)}

Chunk analyses:
----------------

{json.dumps(serialized, indent=2, ensure_ascii=False)}

----------------

Create a research synthesis using ONLY the information above.

Return JSON using exactly this structure:

{{
  "topic": "{topic}",
  "main_findings": [],
  "problems": [],
  "methods": [],
  "datasets": [],
  "metrics": [],
  "results": [],
  "limitations": [],
  "technical_concepts": [],
  "evidence": [],
  "research_gaps": []
}}

Each item should preferably have this structure:

{{
  "text": "...",
  "evidence": "...",
  "pages": {{
    "start": 1,
    "end": 2
  }}
}}

For research_gaps:

Only include gaps that are explicitly supported by the
provided chunk analyses or their limitations.

Do not infer a research gap merely because information is missing.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    text = response.text.strip()

    # Remove accidental markdown code fences.
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        return json.loads(text)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini returned invalid synthesis JSON:\n{text}"
        ) from exc