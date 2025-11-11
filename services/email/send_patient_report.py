import os
from datetime import datetime
from typing import Dict

from flask import current_app
from flask_mail import Message

from models.doctor.operations.get_doctor_by_id import get_doctor_by_id
from models.health_tracker_log.operations.get_health_tracker_logs_by_date_range import \
    get_health_tracker_logs_by_date_range
from models.medication_log.operations.get_medication_logs_by_date_range import get_medication_logs_by_date_range
from models.user.operations.get_user_by_id import get_user_by_id
from services.pdf.generate_patient_report import PatientReportGenerator


class PatientReportEmailService:

    def __init__(self, language: str = "en-US"):
        from flask_mail import Mail
        self.mail = Mail()
        self.language = language
        self.translations = self._get_translations()

    def _get_translations(self) -> Dict[str, Dict[str, str]]:
        return {
            "en-US": {
                "email_subject": "Patient Report - {patient_name} ({start_date} to {end_date})",
                "email_greeting": "Dear Dr. {doctor_name},",
                "email_body_intro": "Please find attached the medical report for patient {patient_name} covering the period from {start_date} to {end_date}.",
                "email_body_content": "This report includes:\n- Medication logs and adherence\n- Health tracker data\n- Patient information and demographics",
                "email_body_instruction": "Please review the report and contact the patient if any follow-up is required.",
                "email_signature": "Best regards,\nMedication Management System"
            },
            "ru-RU": {
                "email_subject": "Отчет о пациенте - {patient_name} ({start_date} - {end_date})",
                "email_greeting": "Уважаемый доктор {doctor_name},",
                "email_body_intro": "Во вложении находится медицинский отчет для пациента {patient_name} за период с {start_date} по {end_date}.",
                "email_body_content": "Отчет включает:\n- Журнал приема лекарств и соблюдение режима\n- Данные мониторинга здоровья\n- Информацию о пациенте и демографические данные",
                "email_body_instruction": "Пожалуйста, ознакомьтесь с отчетом и свяжитесь с пациентом, если требуется дополнительное наблюдение.",
                "email_signature": "С уважением,\nСистема управления лекарствами"
            }
        }

    def _t(self, key: str) -> str:
        return self.translations.get(self.language, self.translations["en-US"]).get(key, key)

    def _format_date(self, date_obj: datetime, format_type: str = "short") -> str:
        if self.language == "ru-RU":
            if format_type == "long":
                month_names = {
                    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                    5: "мая", 6: "июня", 7: "июля", 8: "августа",
                    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
                }
                return f"{date_obj.day} {month_names[date_obj.month]} {date_obj.year}"
            else:
                return date_obj.strftime('%d.%m.%Y')
        else:
            if format_type == "long":
                return date_obj.strftime('%B %d, %Y')
            else:
                return date_obj.strftime('%Y-%m-%d')

    def send_patient_report_to_doctor(self, doctor_id: int, patient_user_id: int,
                                      start_date: datetime, end_date: datetime,
                                      language: str = "en-US") -> dict:
        try:
            if language != self.language:
                self.language = language
                self.translations = self._get_translations()

            doctor = get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                return {
                    'success': False,
                    'error': 'Doctor not found'
                }

            patient_user = get_user_by_id(user_id=patient_user_id)
            if not patient_user:
                return {
                    'success': False,
                    'error': 'Patient user not found'
                }

            medication_logs = get_medication_logs_by_date_range(
                user_id=patient_user_id,
                start_date=start_date,
                end_date=end_date
            )

            health_tracker_logs = get_health_tracker_logs_by_date_range(
                user_id=patient_user_id,
                start_date=start_date,
                end_date=end_date
            )

            pdf_generator = PatientReportGenerator(language=language)
            pdf_file_path = pdf_generator.generate_report(
                user=patient_user,
                medication_logs=medication_logs,
                health_tracker_logs=health_tracker_logs,
                start_date=start_date,
                end_date=end_date
            )

            result = self._send_email_with_pdf(
                doctor_email=doctor.user.email,
                doctor_name=doctor.user.full_name,
                patient_name=patient_user.full_name,
                start_date=start_date,
                end_date=end_date,
                pdf_file_path=pdf_file_path
            )

            try:
                os.unlink(pdf_file_path)
            except OSError:
                pass

            return result

        except Exception as e:
            current_app.logger.error(f"Patient report email failed: {str(e)}")
            current_app.logger.error(f"Doctor ID: {doctor_id}, Patient ID: {patient_user_id}")

            return {
                'success': False,
                'error': f'Failed to send report: {str(e)}'
            }

    def _send_email_with_pdf(self, doctor_email: str, doctor_name: str,
                             patient_name: str, start_date: datetime,
                             end_date: datetime, pdf_file_path: str) -> dict:
        try:
            start_date_str = self._format_date(start_date, "short")
            end_date_str = self._format_date(end_date, "short")
            start_date_long = self._format_date(start_date, "long")
            end_date_long = self._format_date(end_date, "long")

            subject = self._t("email_subject").format(
                patient_name=patient_name,
                start_date=start_date_str,
                end_date=end_date_str
            )

            body = f"""{self._t("email_greeting").format(doctor_name=doctor_name)}

{self._t("email_body_intro").format(patient_name=patient_name, start_date=start_date_long, end_date=end_date_long)}

{self._t("email_body_content")}

{self._t("email_body_instruction")}

{self._t("email_signature")}
            """.strip()

            msg = Message(
                subject=subject,
                recipients=[doctor_email],
                body=body,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@medicationapp.com')
            )

            with open(pdf_file_path, 'rb') as pdf_file:
                msg.attach(
                    filename=f"patient_report_{patient_name}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.pdf",
                    content_type='application/pdf',
                    data=pdf_file.read()
                )

            from app import mail
            mail.send(msg)

            return {
                'success': True,
                'message': f'Report successfully sent to Dr. {doctor_name} at {doctor_email}'
            }

        except Exception as e:
            current_app.logger.error(f"Email sending failed: {str(e)}")
            current_app.logger.error(
                f"Email config - Server: {current_app.config.get('MAIL_SERVER')}, Port: {current_app.config.get('MAIL_PORT')}, Username: {current_app.config.get('MAIL_USERNAME')}")

            return {
                'success': False,
                'error': f'Failed to send email: {str(e)}'
            }
