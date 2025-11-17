from flask import Blueprint, jsonify, request

from models.doctor.operations.get_doctor_by_user_id import get_doctor_by_user_id
from models.patient.operations.create_patient import create_patient
from models.patient.operations.delete_patient import delete_patient
from models.patient.operations.get_patients_by_doctor_id import get_patients_by_doctor_id
from models.patient.operations.get_patients_by_user_id import get_patients_by_user_id
from models.patient.operations.get_pending_patients_by_doctor_id import get_pending_patients_by_doctor_id
from models.patient.operations.get_pending_patients_by_user_id import get_pending_patients_by_user_id
from models.patient.operations.approve_patient import approve_patient
from models.patient.operations.decline_patient import decline_patient
from models.patient.operations.get_patient_by_user_and_doctor import get_patient_by_user_and_doctor
from models.patient.operations.cancel_pending_request import cancel_pending_request
from models.patient.validations import (
    PatientCreateRequest, PatientResponse, RemoveDoctorRequest,
    ApprovePatientRequest, DeclinePatientRequest
)
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request, BODY

# Create Blueprint for patients API
api_patients = Blueprint('/api/patients', __name__)


@api_patients.route('/become-patient', methods=['POST'])
@validate_request(BODY, PatientCreateRequest)
@token_required
def link_patient_to_doctor(user):
    validated_data = request.json

    """
    Link a user to a doctor (create patient-doctor relationship).
    
    Request Body:
        doctor_id: ID of the doctor to link to
    
    Returns:
        JSON response with created patient relationship data
    """
    try:
        doctor_id = validated_data['doctor_id']

        # Create patient-doctor relationship
        patient = create_patient(user_id=user.id, doctor_id=doctor_id)

        # Convert to response format
        patient_response = PatientResponse(
            id=patient.id,
            user_id=patient.user_id,
            doctor_id=patient.doctor_id,
            status=patient.status
        )

        return jsonify({
            'success': True,
            'message': 'Successfully linked to doctor',
            'patient': patient_response.dict()
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/relationship-status/<int:doctor_id>', methods=['GET'])
@token_required
def get_relationship_status(user, doctor_id):
    """
    Get the status of the patient-doctor relationship for the current user and a specific doctor.
    
    Path Parameters:
        doctor_id: ID of the doctor
    
    Returns:
        JSON response with relationship status (pending, approved, or null if no relationship exists)
    """
    try:
        patient = get_patient_by_user_and_doctor(user_id=user.id, doctor_id=doctor_id)
        
        if not patient:
            return jsonify({
                'success': True,
                'status': None,
                'message': 'No relationship exists'
            }), 200
        
        return jsonify({
            'success': True,
            'status': patient.status.value,
            'patient_id': patient.id
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/my-doctors', methods=['GET'])
@token_required
def get_user_doctors(user):
    """
    Get all doctors linked to the current user.
    
    Returns:
        JSON response with list of doctors for the current user
    """
    try:
        # Get all patient relationships for the user
        patients = get_patients_by_user_id(user_id=user.id)

        # Convert to response format
        patients_data = []
        for patient in patients:
            patient_data = {
                'id': patient.id,
                'user_id': patient.user_id,
                'doctor_id': patient.doctor_id,
                'doctor': {
                    'id': patient.doctor.id,
                    'user_id': patient.doctor.user_id,
                    'specialisation': patient.doctor.specialisation,
                    'place_of_work': patient.doctor.place_of_work,
                    'phone': patient.doctor.phone,
                    'photo_url': patient.doctor.photo_url,
                    'user': {
                        'id': patient.doctor.user.id,
                        'full_name': patient.doctor.user.full_name,
                        'email': patient.doctor.user.email,
                        'is_guest': patient.doctor.user.is_guest
                    }
                }
            }
            patients_data.append(patient_data)

        return jsonify({
            'success': True,
            'patients': patients_data,
            'total': len(patients_data)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/my-pending-requests', methods=['GET'])
@token_required
def get_my_pending_requests(user):
    """
    Get all pending patient requests sent by the current user.
    This endpoint is for users to see their own pending requests.
    
    Returns:
        JSON response with list of pending requests
    """
    try:
        # Get all pending patients for this user
        pending_patients = get_pending_patients_by_user_id(user_id=user.id)

        # Convert to response format
        patients_data = []
        for patient in pending_patients:
            patient_data = {
                'id': patient.id,
                'user_id': patient.user_id,
                'doctor_id': patient.doctor_id,
                'status': patient.status.value,
                'doctor': {
                    'id': patient.doctor.id,
                    'user_id': patient.doctor.user_id,
                    'specialisation': patient.doctor.specialisation,
                    'place_of_work': patient.doctor.place_of_work,
                    'phone': patient.doctor.phone,
                    'photo_url': patient.doctor.photo_url,
                    'user': {
                        'id': patient.doctor.user.id,
                        'full_name': patient.doctor.user.full_name,
                        'email': patient.doctor.user.email,
                        'is_guest': patient.doctor.user.is_guest
                    }
                }
            }
            patients_data.append(patient_data)

        return jsonify({
            'success': True,
            'patients': patients_data,
            'total': len(patients_data)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/<int:doctor_id>', methods=['DELETE'])
@token_required
def unlink_patient_from_doctor(user, doctor_id):
    """
    Unlink a user from a doctor (delete patient-doctor relationship).
    
    Path Parameters:
        doctor_id: ID of the doctor to unlink from
    
    Returns:
        JSON response with deletion status
    """
    try:
        # Delete patient-doctor relationship
        deleted = delete_patient(user_id=user.id, doctor_id=doctor_id)

        if not deleted:
            return jsonify({
                'success': False,
                'error': 'Patient-doctor relationship not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Successfully unlinked from doctor'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/remove-doctor', methods=['POST'])
@validate_request(BODY, RemoveDoctorRequest)
@token_required
def remove_doctor(user):
    """
    Remove a doctor from being a doctor for the current user.
    
    Request Body:
        doctor_id: ID of the doctor to remove
    
    Returns:
        JSON response with removal status
    """
    try:
        validated_data = request.json
        doctor_id = validated_data['doctor_id']

        # Delete patient-doctor relationship
        deleted = delete_patient(user_id=user.id, doctor_id=doctor_id)

        if not deleted:
            return jsonify({
                'success': False,
                'error': 'Patient-doctor relationship not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Successfully removed doctor'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/', methods=['GET'])
@token_required
def get_patients_for_doctor(user):
    """
    Get all patients for the current user's doctor.
    This endpoint is for doctors to see their patients.
    
    Returns:
        JSON response with list of user models for the doctor's patients
    """
    try:
        # Get the current user's doctor information
        doctor = get_doctor_by_user_id(user_id=user.id)

        if not doctor:
            return jsonify({
                'success': False,
                'error': 'User is not a doctor'
            }), 403

        # Get all patients for this doctor
        patients = get_patients_by_doctor_id(doctor_id=doctor.id)

        # Extract user models from patient relationships
        users_data = []
        for patient in patients:
            user_data = {
                'id': patient.user.id,
                'uuid': str(patient.user.uuid),
                'full_name': patient.user.full_name,
                'email': patient.user.email,
                'is_guest': patient.user.is_guest,
                'sex': patient.user.sex,
                'date_of_birth': patient.user.date_of_birth.isoformat() if patient.user.date_of_birth else None
            }
            users_data.append(user_data)

        return jsonify({
            'success': True,
            'patients': users_data,
            'total': len(users_data)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/pending-requests', methods=['GET'])
@token_required
def get_pending_requests(user):
    """
    Get all pending patient requests for the current user's doctor.
    This endpoint is for doctors to see pending requests.
    
    Returns:
        JSON response with list of pending patient requests
    """
    try:
        # Get the current user's doctor information
        doctor = get_doctor_by_user_id(user_id=user.id)

        if not doctor:
            return jsonify({
                'success': False,
                'error': 'User is not a doctor'
            }), 403

        # Get all pending patients for this doctor
        pending_patients = get_pending_patients_by_doctor_id(doctor_id=doctor.id)

        # Convert to response format
        patients_data = []
        for patient in pending_patients:
            patient_data = {
                'id': patient.id,
                'user_id': patient.user_id,
                'doctor_id': patient.doctor_id,
                'status': patient.status.value,
                'user': {
                    'id': patient.user.id,
                    'uuid': str(patient.user.uuid),
                    'full_name': patient.user.full_name,
                    'email': patient.user.email,
                    'is_guest': patient.user.is_guest,
                    'sex': patient.user.sex,
                    'date_of_birth': patient.user.date_of_birth.isoformat() if patient.user.date_of_birth else None
                }
            }
            patients_data.append(patient_data)

        return jsonify({
            'success': True,
            'patients': patients_data,
            'total': len(patients_data)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/approve', methods=['POST'])
@validate_request(BODY, ApprovePatientRequest)
@token_required
def approve_patient_request(user):
    """
    Approve a pending patient request.
    This endpoint is for doctors to approve patient requests.
    
    Request Body:
        patient_id: ID of the patient relationship to approve
    
    Returns:
        JSON response with approved patient relationship data
    """
    try:
        # Get the current user's doctor information
        doctor = get_doctor_by_user_id(user_id=user.id)

        if not doctor:
            return jsonify({
                'success': False,
                'error': 'User is not a doctor'
            }), 403

        validated_data = request.json
        patient_id = validated_data['patient_id']

        # Approve the patient request
        patient = approve_patient(patient_id=patient_id, doctor_id=doctor.id)

        # Convert to response format
        patient_response = PatientResponse(
            id=patient.id,
            user_id=patient.user_id,
            doctor_id=patient.doctor_id,
            status=patient.status
        )

        return jsonify({
            'success': True,
            'message': 'Patient request approved successfully',
            'patient': patient_response.dict()
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/decline', methods=['POST'])
@validate_request(BODY, DeclinePatientRequest)
@token_required
def decline_patient_request(user):
    """
    Decline a pending patient request.
    This endpoint is for doctors to decline patient requests.
    The request will be removed from the database.
    
    Request Body:
        patient_id: ID of the patient relationship to decline
    
    Returns:
        JSON response with decline status
    """
    try:
        # Get the current user's doctor information
        doctor = get_doctor_by_user_id(user_id=user.id)

        if not doctor:
            return jsonify({
                'success': False,
                'error': 'User is not a doctor'
            }), 403

        validated_data = request.json
        patient_id = validated_data['patient_id']

        # Decline the patient request (removes it from DB)
        decline_patient(patient_id=patient_id, doctor_id=doctor.id)

        return jsonify({
            'success': True,
            'message': 'Patient request declined successfully'
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_patients.route('/cancel-request', methods=['POST'])
@validate_request(BODY, RemoveDoctorRequest)
@token_required
def cancel_request(user):
    """
    Cancel a pending patient request.
    This endpoint is for users to cancel their own pending requests.
    The request will be removed from the database.
    
    Request Body:
        doctor_id: ID of the doctor whose request to cancel
    
    Returns:
        JSON response with cancellation status
    """
    try:
        validated_data = request.json
        doctor_id = validated_data['doctor_id']

        # Cancel the pending request (removes it from DB)
        cancel_pending_request(user_id=user.id, doctor_id=doctor_id)

        return jsonify({
            'success': True,
            'message': 'Pending request canceled successfully'
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
