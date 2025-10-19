from models.chat_message.chat_message import ChatMessage
from models.doctor.doctor import Doctor
from models.health_tracker.health_tracker import HealthTracker
from models.health_tracker_log.health_tracker_log import HealthTrackerLog
from models.health_tracker_schedule.health_tracker_schedule import HealthTrackerSchedule
from models.medication_log.medication_log import MedicationLog
from models.medicine.medicine import Medicine
from models.medicine_schedule.medicine_schedule import MedicineSchedule
from models.patient.patient import Patient
from models.user.user import User

all_models = [User, Medicine, MedicineSchedule, MedicationLog, HealthTracker, HealthTrackerSchedule, HealthTrackerLog, Doctor, Patient, ChatMessage]
