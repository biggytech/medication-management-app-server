from flask import Blueprint, request, jsonify

from models.doctor.operations.get_doctor_by_id import get_doctor_by_id
from models.doctor.operations.get_doctors import get_doctors
from models.doctor.operations.search_doctors_by_name import search_doctors_by_name
from models.doctor.validations import SearchDoctorsValidation
from services.routers.decorators.token_required import token_required

# Create Blueprint for doctors API
api_doctors = Blueprint('/api/doctors', __name__)


@api_doctors.route('/', methods=['GET'])
@token_required
def search_doctors(user):
    """
    Search doctors by name or get all doctors.
    
    Query Parameters:
        name: Search query for doctor's name (optional)
    
    Returns:
        JSON response with list of doctors matching search criteria
    """
    try:
        name = request.args.get('name')

        # Validate request parameters
        validation_data = SearchDoctorsValidation(
            name=name
        )

        # Get search parameters
        # Search doctors by name if name query provided, otherwise get all doctors
        if name:
            doctors = search_doctors_by_name(name_query=name, exclude_user_id=user.id)
            doctors_list = doctors
        else:
            result = get_doctors()
            doctors_list = result['items'] if isinstance(result, dict) else result

        # Convert doctors to JSON-serializable format
        doctors_data = []
        for doctor in doctors_list:
            doctor_data = {
                'id': doctor.id,
                'user_id': doctor.user_id,
                'specialisation': doctor.specialisation,
                'place_of_work': doctor.place_of_work,
                'phone': doctor.phone,
                'photo_url': doctor.photo_url,
                'user': {
                    'id': doctor.user.id,
                    'full_name': doctor.user.full_name,
                    'email': doctor.user.email,
                    'is_guest': doctor.user.is_guest
                }
            }
            doctors_data.append(doctor_data)

        return jsonify({
            'success': True,
            'doctors': doctors_data,
            'total': len(doctors_data)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_doctors.route('/<int:doctor_id>', methods=['GET'])
# @validate_request(GetDoctorByIdValidation)
@token_required
def get_doctor_by_id_endpoint(user, doctor_id):
    """
    Get a doctor by their ID.
    
    Path Parameters:
        doctor_id: ID of the doctor to retrieve
    
    Returns:
        JSON response with doctor data or error if not found
    """
    try:
        # Get doctor by ID
        doctor = get_doctor_by_id(doctor_id=doctor_id)

        if not doctor:
            return jsonify({
                'success': False,
                'error': 'Doctor not found'
            }), 404

        # Convert doctor to JSON-serializable format (same structure as search API)
        doctor_data = {
            'id': doctor.id,
            'user_id': doctor.user_id,
            'specialisation': doctor.specialisation,
            'place_of_work': doctor.place_of_work,
            'phone': doctor.phone,
            'photo_url': doctor.photo_url,
            'user': {
                'id': doctor.user.id,
                'full_name': doctor.user.full_name,
                'email': doctor.user.email,
                'is_guest': doctor.user.is_guest
            }
        }

        return jsonify({
            'success': True,
            'doctor': doctor_data
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
