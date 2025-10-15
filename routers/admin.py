import os
from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

admin = Blueprint('admin', __name__)

# Admin credentials from environment
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

def admin_required(f):
    """Decorator to require admin authentication"""
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin/login.html')

@admin.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

@admin.route('/')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/users')
@admin_required
def users():
    return render_template('admin/users.html')

@admin.route('/doctors')
@admin_required
def doctors():
    return render_template('admin/doctors.html')

# API routes for user management
@admin.route('/api/users', methods=['GET'])
@admin_required
def api_get_users():
    from models.user.operations.get_users import get_users
    users = get_users()
    return jsonify([{
        'id': user.id,
        'uuid': str(user.uuid),
        'full_name': user.full_name,
        'email': user.email,
        'is_guest': user.is_guest
    } for user in users])

@admin.route('/api/users', methods=['POST'])
@admin_required
def api_create_user():
    from models.user.operations.create_user import create_user
    from models.user.validations import CreateUserValidation
    
    try:
        data = request.get_json()
        validation = CreateUserValidation(**data)
        
        user_result = create_user(
            full_name=validation.full_name,
            email=validation.email,
            password=validation.password,
            is_guest=False
        )
        
        # create_user returns a dict, so we need to get the user object to access other fields
        from models.user.operations.get_user_by_id import get_user_by_id
        user = get_user_by_id(user_result['id'])
        
        return jsonify({
            'id': user.id,
            'uuid': str(user.uuid),
            'full_name': user.full_name,
            'email': user.email,
            'is_guest': user.is_guest
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def api_update_user(user_id):
    from models.user.operations.update_user import update_user
    from models.user.operations.get_user_by_id import get_user_by_id
    
    try:
        data = request.get_json()
        
        # Check if user exists
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update user
        update_result = update_user(
            user=user,
            full_name=data.get('full_name'),
            email=data.get('email'),
            password=data.get('password')
        )
        
        # update_user returns a dict, so we need to get the updated user object
        updated_user = get_user_by_id(user_id)
        
        return jsonify({
            'id': updated_user.id,
            'uuid': str(updated_user.uuid),
            'full_name': updated_user.full_name,
            'email': updated_user.email,
            'is_guest': updated_user.is_guest
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def api_delete_user(user_id):
    from models.user.operations.delete_user import delete_user
    
    try:
        delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API routes for doctor management
@admin.route('/api/doctors', methods=['GET'])
@admin_required
def api_get_doctors():
    from models.doctor.operations.get_doctors import get_doctors
    doctors = get_doctors()
    return jsonify([{
        'id': doctor.id,
        'user_id': doctor.user_id,
        'specialisation': doctor.specialisation,
        'place_of_work': doctor.place_of_work,
        'photo_url': doctor.photo_url,
        'user': {
            'id': doctor.user.id,
            'full_name': doctor.user.full_name,
            'email': doctor.user.email
        }
    } for doctor in doctors])

@admin.route('/api/doctors', methods=['POST'])
@admin_required
def api_create_doctor():
    from models.doctor.operations.create_doctor import create_doctor
    from models.doctor.validations import CreateDoctorValidation
    
    try:
        data = request.get_json()
        validation = CreateDoctorValidation(**data)
        
        doctor = create_doctor(
            user_id=validation.user_id,
            specialisation=validation.specialisation,
            place_of_work=validation.place_of_work,
            photo_url=validation.photo_url
        )
        
        return jsonify({
            'id': doctor.id,
            'user_id': doctor.user_id,
            'specialisation': doctor.specialisation,
            'place_of_work': doctor.place_of_work,
            'photo_url': doctor.photo_url
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin.route('/api/doctors/<int:doctor_id>', methods=['PUT'])
@admin_required
def api_update_doctor(doctor_id):
    from models.doctor.operations.update_doctor import update_doctor
    from models.doctor.operations.get_doctor_by_id import get_doctor_by_id
    
    try:
        data = request.get_json()
        
        # Check if doctor exists
        doctor = get_doctor_by_id(doctor_id)
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        # Update doctor
        updated_doctor = update_doctor(
            doctor_id=doctor_id,
            specialisation=data.get('specialisation'),
            place_of_work=data.get('place_of_work'),
            photo_url=data.get('photo_url')
        )
        
        return jsonify({
            'id': updated_doctor.id,
            'user_id': updated_doctor.user_id,
            'specialisation': updated_doctor.specialisation,
            'place_of_work': updated_doctor.place_of_work,
            'photo_url': updated_doctor.photo_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
@admin_required
def api_delete_doctor(doctor_id):
    from models.doctor.operations.delete_doctor_by_id import delete_doctor_by_id
    
    try:
        delete_doctor_by_id(doctor_id)
        return jsonify({'message': 'Doctor deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
