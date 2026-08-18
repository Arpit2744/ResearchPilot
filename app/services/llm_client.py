import json
import os

from dotenv import load_dotenv
from google import genai
from mistralai.client import Mistral


load_dotenv()


# --------------------------------------------------
# GEMINI
# --------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY not found in .env"
    )

gemini_client = genai.Client(
    api_key=GOOGLE_API_KEY
)

GEMINI_MODEL = "gemini-3.6-flash"


# --------------------------------------------------
# MISTRAL
# --------------------------------------------------

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise RuntimeError(
        "MISTRAL_API_KEY not found in .env"
    )

mistral_client = Mistral(
    api_key=MISTRAL_API_KEY
)

MISTRAL_MODEL = os.getenv(
    "MISTRAL_MODEL",
    "mistral-small-latest",
)


# --------------------------------------------------
# JSON CLEANING
# --------------------------------------------------

def _clean_json_text(text: str) -> str:
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
            1,
        )

        text = text.strip()

    return text


# --------------------------------------------------
# GEMINI REQUEST
# --------------------------------------------------

def _generate_with_gemini(prompt: str) -> str:

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# --------------------------------------------------
# MISTRAL REQUEST
# --------------------------------------------------

def _generate_with_mistral(prompt: str) -> str:

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

    return text.strip()


# --------------------------------------------------
# MAIN LLM FUNCTION
# --------------------------------------------------

def generate_json(prompt: str) -> dict:
    """
    Generate structured JSON using:

        1. Gemini
        2. Mistral fallback

    Gemini is always attempted first.

    Mistral is used if Gemini fails.
    """

    # --------------------------------------------------
    # PRIMARY: GEMINI
    # --------------------------------------------------

    try:

        print(
            "        → LLM provider: Gemini"
        )

        text = _generate_with_gemini(
            prompt
        )

        text = _clean_json_text(
            text
        )

        return json.loads(text)

    except Exception as gemini_error:

        print(
            "        ⚠ Gemini failed."
        )

        print(
            f"          {type(gemini_error).__name__}: "
            f"{gemini_error}"
        )

        print(
            "        → Falling back to Mistral..."
        )

    # --------------------------------------------------
    # FALLBACK: MISTRAL
    # --------------------------------------------------

    try:

        text = _generate_with_mistral(
            prompt
        )

        text = _clean_json_text(
            text
        )

        result = json.loads(text)

        print(
            "        ✓ Mistral fallback succeeded"
        )

        return result

    except Exception as mistral_error:

        raise RuntimeError(
            "Both Gemini and Mistral failed.\n\n"
            f"Gemini error:\n"
            f"{gemini_error}\n\n"
            f"Mistral error:\n"
            f"{mistral_error}"
        ) from mistral_error