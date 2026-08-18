import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_paper(paper_text: str) -> str:
    """
    Analyze extracted research paper text using Gemini.
    """

    if not paper_text.strip():
        raise ValueError("Paper text is empty.")

    prompt = f"""
You are ResearchPilot, a research paper analysis assistant.

Analyze the following research paper.

Extract ONLY information supported by the paper text.
Do not invent missing datasets, experiments, results, or claims.

Structure your response using exactly these sections:

1. Problem
2. Motivation
3. Key Contributions
4. Method
5. Dataset / Data
6. Baselines
7. Evaluation Metrics
8. Results
9. Limitations
10. Future Work

For sections where the paper does not provide enough information,
write:

"Not clearly specified in the provided text."

Be technically precise but concise.

PAPER TEXT:
----------------
{paper_text}
----------------
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text