from sqlalchemy import Column, Integer, String, Text, JSON
from app.database import Base

class IntakeRecord(Base):
    __tablename__ = "intake_records"

    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(Text, nullable=False)
    study_title = Column(String(255), nullable=False)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    primary_conditions = Column(JSON, default=list)
    inclusion_criteria = Column(JSON, default=list)
    exclusion_criteria = Column(JSON, default=list)
    biomarkers_or_labs = Column(JSON, default=list)
