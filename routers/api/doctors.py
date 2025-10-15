from flask import Blueprint, request, jsonify

from models.doctor.operations.get_doctors import get_doctors
from models.doctor.operations.search_doctors_by_name import search_doctors_by_name
from models.doctor.validations import SearchDoctorsValidation
from services.routers.decorators.token_required import token_required
from services.routers.decorators.validate_request import validate_request

# Create Blueprint for doctors API
api_doctors = Blueprint('api_doctors', __name__)


@api_doctors.route('/api/doctors', methods=['GET'])
@token_required
def search_doctors():
    """
    Search doctors by name or get all doctors.
    
    Query Parameters:
        name: Search query for doctor's name (optional)
    
    Returns:
        JSON response with list of doctors matching search criteria
    """
    try:
        # Validate request parameters
        validation_data = SearchDoctorsValidation(
            name=request.args.get('name')
        )
        
        # Get search parameters
        name_query = validation_data.name
        
        # Search doctors by name if name query provided, otherwise get all doctors
        if name_query:
            doctors = search_doctors_by_name(name_query=name_query)
        else:
            doctors = get_doctors()
        
        # Convert doctors to JSON-serializable format
        doctors_data = []
        for doctor in doctors:
            doctor_data = {
                'id': doctor.id,
                'user_id': doctor.user_id,
                'specialisation': doctor.specialisation,
                'place_of_work': doctor.place_of_work,
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
