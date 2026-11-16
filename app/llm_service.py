import os
from google import genai
from google.genai import types
from app.schemas import ClinicalCriteriaExtraction

def _mock_demo_extraction(raw_text: str) -> ClinicalCriteriaExtraction:
    """Provides a deterministic fallback when GEMINI_API_KEY is not configured."""
    lower_text = raw_text.lower()

    if "diabetes" in lower_text or "a1c" in lower_text:
        return ClinicalCriteriaExtraction(
            study_title="Phase III Type 2 Diabetes Glycemic Control Study (Demo Mode)",
            min_age=18,
            max_age=75,
            primary_conditions=["Type 2 Diabetes Mellitus"],
            inclusion_criteria=[
                "Confirmed diagnosis of Type 2 Diabetes for at least 6 months",
                "Stable metformin monotherapy for >= 8 weeks prior to screening",
            ],
            exclusion_criteria=[
                "History of Type 1 Diabetes or diabetic ketoacidosis",
                "eGFR < 45 mL/min/1.73m2",
                "Pregnancy or lactation",
            ],
            biomarkers_or_labs=["HbA1c between 7.5% and 10.5%", "BMI 25.0 - 40.0 kg/m2"],
        )

    return ClinicalCriteriaExtraction(
        study_title="Oncology Biomarker & Immunotherapy Eligibility Protocol (Demo Mode)",
        min_age=21,
        max_age=None,
        primary_conditions=["Non-Small Cell Lung Cancer (NSCLC)", "Advanced Solid Tumors"],
        inclusion_criteria=[
            "Histologically confirmed Stage IIIB or IV disease",
            "ECOG Performance Status of 0 or 1",
            "At least one measurable lesion per RECIST v1.1",
        ],
        exclusion_criteria=[
            "Active untreated CNS metastases",
            "Prior systemic immunotherapy within 4 weeks of enrollment",
            "Active autoimmune disease requiring systemic immunosuppression",
        ],
        biomarkers_or_labs=["PD-L1 TPS >= 50%", "Absolute Neutrophil Count >= 1,500/uL"],
    )

def extract_clinical_criteria(raw_text: str) -> ClinicalCriteriaExtraction:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    # Run in Demo Mode if no real API key is provided
    if not api_key or api_key.lower() in {"demo", "your_gemini_api_key_here"}:
        return _mock_demo_extraction(raw_text)

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
            temperature=0.1,
        ),
    )

    return ClinicalCriteriaExtraction.model_validate_json(response.text)
