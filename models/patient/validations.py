from pydantic import BaseModel, Field
from typing import Optional


class PatientCreateRequest(BaseModel):
    """Request schema for creating a patient-doctor relationship"""
    doctor_id: int = Field(..., description="ID of the doctor to link to")


class PatientResponse(BaseModel):
    """Response schema for patient data"""
    id: int
    user_id: int
    doctor_id: int

    class Config:
        from_attributes = True


class PatientListResponse(BaseModel):
    """Response schema for listing patients"""
    patients: list[PatientResponse]
    total: int


class PatientDeleteResponse(BaseModel):
    """Response schema for patient deletion"""
    message: str
    success: bool
