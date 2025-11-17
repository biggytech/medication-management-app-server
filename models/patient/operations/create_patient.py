from sqlalchemy.orm import Session, joinedload
from models.patient.patient import Patient
from models.doctor.doctor import Doctor
from models.common.enums.patient_request_status import PatientRequestStatus
from services.db.decorators.with_session import with_session


@with_session
def create_patient(session: Session, user_id: int, doctor_id: int) -> Patient:
    """
    Create a new patient-doctor relationship.
    
    Args:
        session: Database session
        user_id: ID of the user (patient)
        doctor_id: ID of the doctor
        
    Returns:
        Patient: The created patient relationship
        
    Raises:
        ValueError: If doctor doesn't exist or relationship already exists
    """
    # Check if doctor exists
    doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise ValueError(f"Doctor with id {doctor_id} not found")
    
    # Check if relationship already exists
    existing_patient = session.query(Patient).filter(
        Patient.user_id == user_id,
        Patient.doctor_id == doctor_id
    ).first()
    
    if existing_patient:
        raise ValueError(f"Patient relationship already exists between user {user_id} and doctor {doctor_id}")
    
    # Create new patient relationship with pending status
    patient = Patient(
        user_id=user_id,
        doctor_id=doctor_id,
        status=PatientRequestStatus.pending
    )
    
    session.add(patient)
    session.commit()
    session.refresh(patient)
    
    # Eagerly load the doctor relationship to avoid lazy loading issues
    patient = session.query(Patient).options(
        joinedload(Patient.doctor).joinedload(Doctor.user)
    ).filter(Patient.id == patient.id).first()
    
    return patient
