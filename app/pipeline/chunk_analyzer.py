import json
import os

from dotenv import load_dotenv
from google import genai
from mistralai.client import Mistral

from ..schemas.evidence import (
    ChunkAnalysis,
    EvidenceItem,
)


load_dotenv()


# ============================================================
# API CONFIGURATION
# ============================================================

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

# Use a Mistral model available to your API account.
MISTRAL_MODEL = "mistral-small-latest"


# ============================================================
# SYSTEM INSTRUCTION
# ============================================================

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

The output must contain ONLY valid JSON.
"""


# ============================================================
# HELPERS
# ============================================================

def _clean_json_response(text: str) -> str:
    """
    Remove accidental markdown code fences from an LLM response.
    """

    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return text


def _to_evidence_items(items) -> list[EvidenceItem]:
    """
    Convert LLM JSON items into EvidenceItem objects.
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
                evidence=str(
                    item.get("evidence", "")
                ),
            )
        )

    return result


def _parse_chunk_analysis(
    data: dict,
    chunk,
) -> ChunkAnalysis:
    """
    Convert normalized LLM JSON into ChunkAnalysis.
    """

    pages = data.get("pages", {})

    if not isinstance(pages, dict):
        pages = {}

    return ChunkAnalysis(
        chunk_id=str(
            data.get(
                "chunk_id",
                chunk.chunk_id,
            )
        ),

        start_page=int(
            pages.get(
                "start",
                chunk.start_page,
            )
        ),

        end_page=int(
            pages.get(
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


# ============================================================
# PROMPT
# ============================================================

def _build_prompt(chunk) -> str:

    return f"""
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


# ============================================================
# GEMINI
# ============================================================

def _analyze_with_gemini(prompt: str) -> dict:

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    text = response.text

    if not text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    text = _clean_json_response(text)

    return json.loads(text)


# ============================================================
# MISTRAL
# ============================================================

def _analyze_with_mistral(prompt: str) -> dict:

    response = mistral_client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format={
            "type": "json_object"
        },
    )

    text = response.choices[0].message.content

    if not text:
        raise ValueError(
            "Mistral returned an empty response."
        )

    text = _clean_json_response(text)

    return json.loads(text)


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_chunk(chunk) -> ChunkAnalysis:

    prompt = _build_prompt(chunk)

    # --------------------------------------------------------
    # PRIMARY: GEMINI
    # --------------------------------------------------------

    try:

        print(
            "        → Trying Gemini..."
        )

        data = _analyze_with_gemini(
            prompt
        )

        print(
            "        ✓ Gemini succeeded"
        )

        return _parse_chunk_analysis(
            data,
            chunk,
        )

    except Exception as gemini_error:

        print(
            f"        ⚠ Gemini failed: "
            f"{type(gemini_error).__name__}"
        )

        print(
            "        → Falling back to Mistral..."
        )

    # --------------------------------------------------------
    # FALLBACK: MISTRAL
    # --------------------------------------------------------

    try:

        data = _analyze_with_mistral(
            prompt
        )

        print(
            "        ✓ Mistral succeeded"
        )

        return _parse_chunk_analysis(
            data,
            chunk,
        )

    except Exception as mistral_error:

        raise RuntimeError(
            "Both Gemini and Mistral failed.\n"
            f"Gemini error: {gemini_error}\n"
            f"Mistral error: {mistral_error}"
        ) from mistral_error