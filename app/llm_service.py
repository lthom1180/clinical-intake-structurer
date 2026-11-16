import os
from google import genai
from google.genai import types
from app.schemas import ClinicalCriteriaExtraction

def extract_clinical_criteria(raw_text: str) -> ClinicalCriteriaExtraction:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    client = genai.Client(api_key=api_key)

    prompt = (
        "You are a clinical research data assistant. Extract structured eligibility "
        "criteria and clinical entities from the following unstructured note. "
        "Only extract facts explicitly present in the text; do not infer or hallucinate.\n\n"
        f"Clinical Note:\n{raw_text}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ClinicalCriteriaExtraction,
            temperature=0.1,  # Low temperature for deterministic extraction
        ),
    )

    return ClinicalCriteriaExtraction.model_validate_json(response.text)
