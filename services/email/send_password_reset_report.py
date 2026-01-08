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


def send_password_reset_report(email, code):
    body = f"""Был запрошен доступ на сброс вашего пароля.

Код подтверждения {code}
    """

    msg = Message(
        subject='Код подтверждения для сброса пароля',
        recipients=[email],
        body=body,
        sender=('Медика', current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@medicationapp.com'))
    )

    from app import mail
    mail.send(msg)
