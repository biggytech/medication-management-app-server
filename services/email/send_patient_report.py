import os
from datetime import datetime

from flask import current_app
from flask_mail import Message

from models.doctor.operations.get_doctor_by_id import get_doctor_by_id
from models.health_tracker_log.operations.get_health_tracker_logs_by_date_range import \
    get_health_tracker_logs_by_date_range
from models.medication_log.operations.get_medication_logs_by_date_range import get_medication_logs_by_date_range
from models.user.operations.get_user_by_id import get_user_by_id
from services.pdf.generate_patient_report import PatientReportGenerator


class PatientReportEmailService:
    """Service for sending patient reports via email to doctors"""

    def __init__(self):
        from flask_mail import Mail
        self.mail = Mail()

    def send_patient_report_to_doctor(self, doctor_id: int, patient_user_id: int,
                                      start_date: datetime, end_date: datetime,
                                      language: str = "en-US") -> dict:
        """
        Send a patient report PDF to a doctor's email.
        
        Args:
            doctor_id: ID of the doctor to send the report to
            patient_user_id: ID of the patient user
            start_date: Start date for the report
            end_date: End date for the report
            language: Language for the report (en-US or ru-RU)
            
        Returns:
            dict: Result with success status and message
        """
        try:
            # Get doctor information
            doctor = get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                return {
                    'success': False,
                    'error': 'Doctor not found'
                }

            # Get patient user data
            patient_user = get_user_by_id(user_id=patient_user_id)
            if not patient_user:
                return {
                    'success': False,
                    'error': 'Patient user not found'
                }

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

            print('pdf_file_path', pdf_file_path)

            print('Sending....')
            # Send email with PDF attachment

            result = self._send_email_with_pdf(
                doctor_email=doctor.user.email,
                doctor_name=doctor.user.full_name,
                patient_name=patient_user.full_name,
                start_date=start_date,
                end_date=end_date,
                pdf_file_path=pdf_file_path
            )

            print('Sent!')

            # Clean up temporary PDF file
            try:
                os.unlink(pdf_file_path)
            except OSError:
                pass  # File might already be deleted

            # return None
            return result

        except Exception as e:
            # Log the specific error for debugging
            current_app.logger.error(f"Patient report email failed: {str(e)}")
            current_app.logger.error(f"Doctor ID: {doctor_id}, Patient ID: {patient_user_id}")

            return {
                'success': False,
                'error': f'Failed to send report: {str(e)}'
            }

    def _send_email_with_pdf(self, doctor_email: str, doctor_name: str,
                             patient_name: str, start_date: datetime,
                             end_date: datetime, pdf_file_path: str) -> dict:
        """
        Send email with PDF attachment to doctor.
        
        Args:
            doctor_email: Doctor's email address
            doctor_name: Doctor's full name
            patient_name: Patient's full name
            start_date: Report start date
            end_date: Report end date
            pdf_file_path: Path to the generated PDF file
            
        Returns:
            dict: Result with success status and message
        """
        try:
            # Create email message
            subject = f"Patient Report - {patient_name} ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})"

            # Create email body
            body = f"""
Dear Dr. {doctor_name},

Please find attached the medical report for patient {patient_name} covering the period from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}.

This report includes:
- Medication logs and adherence
- Health tracker data
- Patient information and demographics

Please review the report and contact the patient if any follow-up is required.

Best regards,
Medication Management System
            """.strip()

            # Create message
            msg = Message(
                subject=subject,
                recipients=[doctor_email],
                body=body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@medicationapp.com')
            )

            # Attach PDF file
            with open(pdf_file_path, 'rb') as pdf_file:
                msg.attach(
                    filename=f"patient_report_{patient_name}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.pdf",
                    content_type='application/pdf',
                    data=pdf_file.read()
                )

            print('Started sending!')

            # Send email using the app's mail instance
            # from flask_mail import Mail
            # mail = Mail(current_app)
            # mail.send(msg)

            from app import mail
            mail.send(msg)

            return {
                'success': True,
                'message': f'Report successfully sent to Dr. {doctor_name} at {doctor_email}'
            }

        except Exception as e:
            # Log the specific error for debugging
            current_app.logger.error(f"Email sending failed: {str(e)}")
            current_app.logger.error(
                f"Email config - Server: {current_app.config.get('MAIL_SERVER')}, Port: {current_app.config.get('MAIL_PORT')}, Username: {current_app.config.get('MAIL_USERNAME')}")

            return {
                'success': False,
                'error': f'Failed to send email: {str(e)}'
            }
