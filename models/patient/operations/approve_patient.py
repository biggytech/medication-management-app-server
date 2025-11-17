from sqlalchemy.orm import Session, joinedload
from models.patient.patient import Patient
from models.doctor.doctor import Doctor
from models.common.enums.patient_request_status import PatientRequestStatus
from services.db.decorators.with_session import with_session


@with_session
def approve_patient(session: Session, patient_id: int, doctor_id: int) -> Patient:
    """
    Approve a pending patient request.
    Changes the status from pending to approved.
    
    Args:
        session: Database session
        patient_id: ID of the patient relationship
        doctor_id: ID of the doctor (for validation)
        
    Returns:
        Patient: The approved patient relationship
        
    Raises:
        ValueError: If patient doesn't exist, doesn't belong to doctor, or is not pending
    """
    # Get the patient relationship
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise ValueError(f"Patient relationship with id {patient_id} not found")
    
    # Verify it belongs to the doctor
    if patient.doctor_id != doctor_id:
        raise ValueError(f"Patient relationship does not belong to doctor {doctor_id}")
    
    # Verify it's pending
    if patient.status != PatientRequestStatus.pending:
        raise ValueError(f"Patient relationship is not pending (current status: {patient.status})")
    
    # Update status to approved
    patient.status = PatientRequestStatus.approved
    session.commit()
    session.refresh(patient)
    
    # Eagerly load the relationships
    patient = session.query(Patient).options(
        joinedload(Patient.doctor).joinedload(Doctor.user),
        joinedload(Patient.user)
    ).filter(Patient.id == patient.id).first()
    
    return patient

