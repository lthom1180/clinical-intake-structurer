from pydantic import BaseModel, Field
from typing import List, Optional

class ClinicalCriteriaExtraction(BaseModel):
    study_title: str = Field(description="Short inferred title or topic of the clinical note")
    min_age: Optional[int] = Field(None, description="Minimum patient age in years, if specified")
    max_age: Optional[int] = Field(None, description="Maximum patient age in years, if specified")
    primary_conditions: List[str] = Field(default_factory=list, description="Target diagnoses or conditions")
    inclusion_criteria: List[str] = Field(default_factory=list, description="Key eligibility requirements")
    exclusion_criteria: List[str] = Field(default_factory=list, description="Conditions or medications that disqualify the patient")
    biomarkers_or_labs: List[str] = Field(default_factory=list, description="Required lab values, genetic markers, or vitals")

class IntakeRequest(BaseModel):
    raw_text: str = Field(..., min_length=20, description="Unstructured clinical trial note or intake summary")

class IntakeRecordResponse(ClinicalCriteriaExtraction):
    id: int
    raw_text: str

    class Config:
        from_attributes = True
