import json
import os
from dataclasses import asdict

from dotenv import load_dotenv
from google import genai
from mistralai.client import Mistral


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
MISTRAL_MODEL = "mistral-small-latest"


# ============================================================
# SYSTEM INSTRUCTION
# ============================================================

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


# ============================================================
# HELPERS
# ============================================================

def _serialize_analyses(analyses) -> list[dict]:
    """
    Convert ChunkAnalysis dataclasses into JSON-compatible dictionaries.
    """

    return [
        asdict(analysis)
        for analysis in analyses
    ]


def _clean_json_response(text: str) -> str:
    """
    Remove accidental markdown code fences.
    """

    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return text


def _build_prompt(
    topic: str,
    analyses: list,
) -> str:
    """
    Build the synthesis prompt shared by Gemini and Mistral.
    """

    serialized = _serialize_analyses(
        analyses
    )

    return f"""
{SYSTEM_INSTRUCTION}

Research topic:
{topic}

Number of analyzed chunks:
{len(analyses)}

Chunk analyses:
----------------

{json.dumps(
    serialized,
    indent=2,
    ensure_ascii=False,
)}

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

Return ONLY valid JSON.
"""


# ============================================================
# GEMINI
# ============================================================

def _synthesize_with_gemini(
    prompt: str,
) -> dict:
    """
    Generate synthesis using Gemini.
    """

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    text = response.text

    if not text:
        raise ValueError(
            "Gemini returned an empty synthesis response."
        )

    text = _clean_json_response(text)

    return json.loads(text)


# ============================================================
# MISTRAL
# ============================================================

def _synthesize_with_mistral(
    prompt: str,
) -> dict:
    """
    Generate synthesis using Mistral.
    """

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
            "Mistral returned an empty synthesis response."
        )

    text = _clean_json_response(text)

    return json.loads(text)


# ============================================================
# MAIN SYNTHESIZER
# ============================================================

def synthesize_analyses(
    topic: str,
    analyses: list,
) -> dict:
    """
    Synthesize multiple ChunkAnalysis objects into a
    research-level summary.

    Provider order:

        Gemini
           ↓
        Mistral fallback

    Both providers return the same JSON structure.
    """

    if not analyses:
        raise ValueError(
            "Cannot synthesize research without chunk analyses."
        )

    prompt = _build_prompt(
        topic=topic,
        analyses=analyses,
    )

    # --------------------------------------------------------
    # PRIMARY: GEMINI
    # --------------------------------------------------------

    try:

        print(
            "      → Trying Gemini for synthesis..."
        )

        result = _synthesize_with_gemini(
            prompt
        )

        print(
            "      ✓ Gemini synthesis succeeded"
        )

        return result

    except Exception as gemini_error:

        print(
            "      ⚠ Gemini synthesis failed: "
            f"{type(gemini_error).__name__}"
        )

        print(
            "      → Falling back to Mistral..."
        )

    # --------------------------------------------------------
    # FALLBACK: MISTRAL
    # --------------------------------------------------------

    try:

        result = _synthesize_with_mistral(
            prompt
        )

        print(
            "      ✓ Mistral synthesis succeeded"
        )

        return result

    except Exception as mistral_error:

        raise RuntimeError(
            "Both Gemini and Mistral failed during synthesis.\n"
            f"Gemini error: {gemini_error}\n"
            f"Mistral error: {mistral_error}"
        ) from mistral_error