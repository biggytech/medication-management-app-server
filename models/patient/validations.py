from pydantic import BaseModel, Field
from typing import Optional
from models.common.enums.patient_request_status import PatientRequestStatus


class PatientCreateRequest(BaseModel):
    """Request schema for creating a patient-doctor relationship"""
    doctor_id: int = Field(..., description="ID of the doctor to link to")


class PatientResponse(BaseModel):
    """Response schema for patient data"""
    id: int
    user_id: int
    doctor_id: int
    status: PatientRequestStatus

    class Config:
        from_attributes = True


class ApprovePatientRequest(BaseModel):
    """Request schema for approving a patient request"""
    patient_id: int = Field(..., description="ID of the patient relationship to approve")


class DeclinePatientRequest(BaseModel):
    """Request schema for declining a patient request"""
    patient_id: int = Field(..., description="ID of the patient relationship to decline")


class PatientListResponse(BaseModel):
    """Response schema for listing patients"""
    patients: list[PatientResponse]
    total: int


class PatientDeleteResponse(BaseModel):
    """Response schema for patient deletion"""
    message: str
    success: bool


class RemoveDoctorRequest(BaseModel):
    """Request schema for removing a doctor from patient relationship"""
    doctor_id: int = Field(..., description="ID of the doctor to remove")
