from datetime import datetime

from flask import Blueprint, jsonify, request, send_file

from models.health_tracker_log.operations.get_health_tracker_logs_by_date_range import \
    get_health_tracker_logs_by_date_range
from models.medication_log.operations.get_medication_logs_by_date_range import get_medication_logs_by_date_range
from models.user.operations.get_user_by_id import get_user_by_id
from services.email.send_patient_report import PatientReportEmailService
from services.pdf.generate_patient_report import PatientReportGenerator
from services.routers.decorators.token_required import token_required

# Create Blueprint for patient reports API
api_patient_reports = Blueprint('/api/patient-reports', __name__)


# class PatientReportRequest(BaseModel):
#     """Validation schema for patient report request"""
#     start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
#     end_date: str = Field(..., description="End date in YYYY-MM-DD format")
#     user_id: int = Field(..., description="ID of the patient user")
#     language: str = Field(default="en-US", description="Language for the report (en-US or ru-RU)")


@api_patient_reports.route('/generate', methods=['GET'])
@token_required
def generate_patient_report(user):
    """
    Generate a PDF report for a patient with medication and health tracking data.
    
    Query Parameters:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        user_id: ID of the patient user
        language: Language for the report (en-US or ru-RU, default: en-US)
    
    Returns:
        JSON response with temporary download link to the generated PDF
    """
    try:
        # Get validated query parameters
        validated_data = request.args

        start_date_str = validated_data['start_date']
        end_date_str = validated_data['end_date']
        # patient_user_id = int(validated_data['user_id'])
        patient_user_id = user.id
        language = validated_data.get('language', 'en-US')

        # Validate language
        if language not in ['en-US', 'ru-RU']:
            return jsonify({
                'success': False,
                'error': 'Invalid language. Supported languages: en-US, ru-RU'
            }), 400

        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD format'
            }), 400

        # Validate date range
        if start_date > end_date:
            return jsonify({
                'success': False,
                'error': 'Start date must be before or equal to end date'
            }), 400

        # Get patient user data
        patient_user = get_user_by_id(user_id=patient_user_id)
        if not patient_user:
            return jsonify({
                'success': False,
                'error': 'Patient user not found'
            }), 404

        # Get medication logs for the date range
        medication_logs = get_medication_logs_by_date_range(
            user_id=patient_user_id,
            start_date=start_date,
            end_date=end_date
        )

        # Get health tracker logs for the date range
        health_tracker_logs = get_health_tracker_logs_by_date_range(
            user_id=patient_user_id,
            start_date=start_date,
            end_date=end_date
        )

        # Generate PDF report
        pdf_generator = PatientReportGenerator(language=language)
        pdf_file_path = pdf_generator.generate_report(
            user=patient_user,
            medication_logs=medication_logs,
            health_tracker_logs=health_tracker_logs,
            start_date=start_date,
            end_date=end_date
        )

        # Generate a temporary filename for download
        temp_filename = f"patient_report_{patient_user_id}_{start_date_str}_{end_date_str}.pdf"

        # Return the file for download
        response = send_file(
            pdf_file_path,
            as_attachment=True,
            download_name=temp_filename,
            mimetype='application/pdf'
        )
        response.direct_passthrough = False
        return response

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate report: {str(e)}'
        }), 500


@api_patient_reports.route('/send-email', methods=['POST'])
@token_required
def send_patient_report_email(user):
    """
    Send a patient report PDF via email to a doctor.
    
    Query Parameters:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        doctor_id: ID of the doctor to send the report to
        language: Language for the report (en-US or ru-RU, default: en-US)
    
    Returns:
        JSON response with success status and message
    """
    try:
        # Get validated query parameters
        validated_data = request.json

        start_date_str = validated_data['start_date']
        end_date_str = validated_data['end_date']
        doctor_id = int(validated_data['doctor_id'])
        patient_user_id = user.id
        language = validated_data.get('language', 'en-US')

        # Validate language
        if language not in ['en-US', 'ru-RU']:
            return jsonify({
                'success': False,
                'error': 'Invalid language. Supported languages: en-US, ru-RU'
            }), 400

        # Parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD format'
            }), 400

        # Validate date range
        if start_date > end_date:
            return jsonify({
                'success': False,
                'error': 'Start date must be before or equal to end date'
            }), 400

        # Send email with patient report
        email_service = PatientReportEmailService()
        result = email_service.send_patient_report_to_doctor(
            doctor_id=doctor_id,
            patient_user_id=patient_user_id,
            start_date=start_date,
            end_date=end_date,
            language=language
        )

        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to send report: {str(e)}'
        }), 500


@api_patient_reports.route('/test-email-config', methods=['GET'])
@token_required
def test_email_config(user):
    """
    Test email configuration and return current settings.
    This endpoint helps debug email configuration issues.
    
    Returns:
        JSON response with email configuration status
    """
    try:
        from flask import current_app

        # Get email configuration
        config = {
            'MAIL_SERVER': current_app.config.get('MAIL_SERVER'),
            'MAIL_PORT': current_app.config.get('MAIL_PORT'),
            'MAIL_USE_TLS': current_app.config.get('MAIL_USE_TLS'),
            'MAIL_USE_SSL': current_app.config.get('MAIL_USE_SSL'),
            'MAIL_USERNAME': current_app.config.get('MAIL_USERNAME'),
            'MAIL_PASSWORD': '***' if current_app.config.get('MAIL_PASSWORD') else None,
            'MAIL_DEFAULT_SENDER': current_app.config.get('MAIL_DEFAULT_SENDER')
        }

        # Check if required settings are present
        missing_required = []
        if not config['MAIL_USERNAME']:
            missing_required.append('MAIL_USERNAME')
        if not current_app.config.get('MAIL_PASSWORD'):
            missing_required.append('MAIL_PASSWORD')

        if missing_required:
            return jsonify({
                'success': False,
                'error': f'Missing required email configuration: {", ".join(missing_required)}',
                'config': config,
                'setup_instructions': {
                    'required_env_vars': ['MAIL_USERNAME', 'MAIL_PASSWORD'],
                    'optional_env_vars': ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USE_TLS', 'MAIL_USE_SSL',
                                          'MAIL_DEFAULT_SENDER'],
                    'example': 'MAIL_USERNAME=your-email@gmail.com MAIL_PASSWORD=your-app-password'
                }
            }), 400

        return jsonify({
            'success': True,
            'message': 'Email configuration looks good',
            'config': config
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to check email configuration: {str(e)}'
        }), 500


@api_patient_reports.route('/download/<filename>', methods=['GET'])
@token_required
def download_report(user, filename):
    """
    Download a previously generated report.
    This endpoint is for future use if we want to implement file caching.
    
    Path Parameters:
        filename: Name of the report file to download
    
    Returns:
        PDF file download
    """
    try:
        # For now, this is a placeholder for future file caching implementation
        return jsonify({
            'success': False,
            'error': 'File not found. Please generate a new report.'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
