import os

from dotenv import load_dotenv
from flask import Flask, request, send_from_directory, Response

# Load environment variables
load_dotenv()

from routers.admin import admin
from routers.api.doctors import api_doctors
from routers.api.health_tracker_logs import api_health_tracker_logs
from routers.api.health_trackers import api_health_trackers
from routers.api.medication_logs import api_medication_logs
from routers.api.medicines import api_medicines
from routers.api.patients import api_patients
from routers.api.patient_reports import api_patient_reports
from routers.api.sign_in.default import api_sign_in_default
from routers.api.sign_out.anonymous import api_sign_out_anonymous
from routers.api.sign_up.anonymous import api_sign_up_anonymous
from routers.api.sign_up.default import api_sign_up_default
from routers.api.users import api_users

app = Flask(__name__)
app.url_map.strict_slashes = False

# Set secret key for sessions
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')


# Useful debugging interceptor to log all values posted to the endpoint
@app.before_request
def before():
    # Skip logging for image requests
    if request.endpoint and 'uploads' in request.endpoint:
        return

    values = 'values: '
    if len(request.values) == 0:
        values += '(None)'
    for key in request.values:
        values += key + ': ' + request.values[key] + ', '
    app.logger.debug(values)


# Useful debugging interceptor to log all endpoint responses
@app.after_request
def after(response):
    # Skip logging for image requests to avoid binary data issues
    if request.endpoint and 'uploads' in request.endpoint:
        return response

    try:
        app.logger.debug('response: ' + response.status + ', ' + response.data.decode('utf-8'))
    except UnicodeDecodeError:
        # Skip logging for binary responses
        app.logger.debug('response: ' + response.status + ', [binary data]')
    return response


# Default handler for uncaught exceptions in the app
@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return Flask.make_response('server error', 500)


# Default handler for all bad requests sent to the app
@app.errorhandler(400)
def handle_bad_request(e):
    app.logger.info('Bad request', e)
    return Flask.make_response('bad request', 400)


# File serving route for uploads (without admin prefix)
@app.route('/uploads/doctors/<filename>')
def serve_uploaded_file(filename):
    """Serve uploaded doctor photos from the main app"""
    try:
        # Use absolute path to avoid issues
        upload_path = os.path.join(os.getcwd(), 'uploads', 'doctors')
        app.logger.debug(f"Serving file: {filename} from {upload_path}")

        # Check if file exists
        file_path = os.path.join(upload_path, filename)
        if not os.path.exists(file_path):
            app.logger.error(f"File not found: {file_path}")
            return Response("File not found", status=404)

        # Serve the file
        response = send_from_directory(upload_path, filename, as_attachment=False)
        response.direct_passthrough = False
        app.logger.debug(f"File served successfully: {filename}")
        return response

    except FileNotFoundError:
        app.logger.error(f"File not found: uploads/doctors/{filename}")
        return Response("File not found", status=404)
    except Exception as e:
        app.logger.error(f"Error serving file {filename}: {str(e)}")
        return Response("Error serving file", status=500)


app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api_doctors, url_prefix='/api/doctors')
app.register_blueprint(api_patients, url_prefix='/api/patients')
app.register_blueprint(api_patient_reports, url_prefix='/api/patient-reports')
app.register_blueprint(api_sign_in_default, url_prefix='/api/sign-in/default')
app.register_blueprint(api_sign_up_anonymous, url_prefix='/api/sign-up/anonymous')
app.register_blueprint(api_sign_up_default, url_prefix='/api/sign-up/default')
app.register_blueprint(api_sign_out_anonymous, url_prefix='/api/sign-out/anonymous')
app.register_blueprint(api_medicines, url_prefix='/api/medicines')
app.register_blueprint(api_medication_logs, url_prefix='/api/medication-logs')
app.register_blueprint(api_health_trackers, url_prefix='/api/health-trackers')
app.register_blueprint(api_health_tracker_logs, url_prefix='/api/health-tracker-logs')
app.register_blueprint(api_users, url_prefix='/api/users')
