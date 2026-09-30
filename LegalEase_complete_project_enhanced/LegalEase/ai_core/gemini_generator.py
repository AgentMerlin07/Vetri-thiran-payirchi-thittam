from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
)


class GeminiDocumentGenerator:
    """Generates structured legal-document drafts from the supplied user inputs."""

    SYSTEM_INSTRUCTION = """
You are LegalEase, an AI legal-document drafting assistant.

Create a professional first-draft legal document from the user's supplied
document type, parties, terms, and effective date.

Rules:
1. Use only facts supplied by the user. Never invent names, addresses,
   amounts, dates, jurisdictions, statutes, or obligations.
2. Use clear professional legal language and conventional sections.
3. Start with the document title.
4. Include the parties and effective date.
5. Organize the document with numbered headings and clauses.
6. Reflect every supplied term. Do not silently remove a requested term.
7. If a detail is missing, use a neutral placeholder such as
   "[NOT PROVIDED]" instead of guessing.
8. Do not claim that the generated document is legally valid, legally sound,
   or a substitute for a qualified lawyer.
9. Return plain text only. Do not use Markdown fences.
10. End with a short "Review Notes" section identifying missing information
    that the user should verify before signing.
"""

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured. Add it to your .env file."
            )
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        if not all(
            isinstance(value, str) and value.strip()
            for value in (document_type, parties, terms, dates)
        ):
            raise ValueError("document_type, parties, terms, and dates are required.")

        prompt = f"""
Document type:
{document_type.strip()}

Parties involved:
{parties.strip()}

Terms and conditions:
{terms.strip()}

Effective date:
{dates.strip()}

Draft the requested document now.
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.SYSTEM_INSTRUCTION,
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                candidate_count=1,
            ),
        )

        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise RuntimeError(
                "Gemini returned no text. Check the model name, API key, "
                "quota, and safety response."
            )
        return text.strip()
