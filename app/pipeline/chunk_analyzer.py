import json
import os

from dotenv import load_dotenv
from google import genai

from ..schemas.evidence import (
    ChunkAnalysis,
    EvidenceItem,
)


load_dotenv()


API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in .env")


client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"


SYSTEM_INSTRUCTION = """
You are a research paper extraction agent.

Analyze ONLY the provided paper chunk.

Do not invent information that is not present in the chunk.

Extract useful research information into structured JSON.

If a field is not supported by the chunk, return an empty list.

Pay particular attention to:
- research claims
- problems
- methods
- datasets
- metrics
- results
- limitations
- important technical concepts
- evidence

Every extracted item should include the exact supporting text as a short quote when possible.
"""


def _to_evidence_items(items) -> list[EvidenceItem]:
    """
    Convert Gemini JSON items into EvidenceItem objects.
    """

    if not isinstance(items, list):
        return []

    result = []

    for item in items:

        if not isinstance(item, dict):
            continue

        text = item.get("text")

        if not text:
            continue

        result.append(
            EvidenceItem(
                text=str(text),
                evidence=str(item.get("evidence", "")),
            )
        )

    return result


def analyze_chunk(chunk) -> ChunkAnalysis:

    prompt = f"""
{SYSTEM_INSTRUCTION}

Paper chunk:
----------------

Chunk ID: {chunk.chunk_id}

Pages: {chunk.start_page}-{chunk.end_page}

Text:

{chunk.text}

----------------

Return ONLY valid JSON using this schema:

{{
  "chunk_id": "{chunk.chunk_id}",
  "pages": {{
    "start": {chunk.start_page},
    "end": {chunk.end_page}
  }},
  "claims": [],
  "problems": [],
  "methods": [],
  "datasets": [],
  "metrics": [],
  "results": [],
  "limitations": [],
  "technical_concepts": [],
  "evidence": []
}}

Each extracted item should preferably have:

{{
  "text": "...",
  "evidence": "short supporting quote"
}}

Do not add information that isn't supported by the chunk.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    text = response.text.strip()

    # Handle accidental markdown fences.
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        data = json.loads(text)

    except json.JSONDecodeError as exc:

        raise ValueError(
            f"Gemini returned invalid JSON:\n{text}"
        ) from exc

    return ChunkAnalysis(
        chunk_id=str(
            data.get("chunk_id", chunk.chunk_id)
        ),

        start_page=int(
            data.get("pages", {}).get(
                "start",
                chunk.start_page,
            )
        ),

        end_page=int(
            data.get("pages", {}).get(
                "end",
                chunk.end_page,
            )
        ),

        claims=_to_evidence_items(
            data.get("claims", [])
        ),

        problems=_to_evidence_items(
            data.get("problems", [])
        ),

        methods=_to_evidence_items(
            data.get("methods", [])
        ),

        datasets=_to_evidence_items(
            data.get("datasets", [])
        ),

        metrics=_to_evidence_items(
            data.get("metrics", [])
        ),

        results=_to_evidence_items(
            data.get("results", [])
        ),

        limitations=_to_evidence_items(
            data.get("limitations", [])
        ),

        technical_concepts=_to_evidence_items(
            data.get("technical_concepts", [])
        ),

        evidence=_to_evidence_items(
            data.get("evidence", [])
        ),
    )