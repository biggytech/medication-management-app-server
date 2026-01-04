    ALTER TABLE health_tracker_logs

DROP CONSTRAINT health_tracker_logs_health_tracker_id_fkey,
ADD CONSTRAINT health_tracker_logs_health_tracker_id_fkey
FOREIGN KEY (health_tracker_id)
REFERENCES health_trackers(id)
ON DELETE CASCADE;

      ALTER TABLE health_tracker_schedules

DROP CONSTRAINT health_tracker_schedules_health_tracker_id_fkey,
ADD CONSTRAINT health_tracker_schedules_health_tracker_id_fkey
FOREIGN KEY (health_tracker_id)
REFERENCES health_trackers(id)
ON DELETE CASCADE;

          ALTER TABLE medication_logs

DROP CONSTRAINT medication_logs_medicine_id_fkey,
ADD CONSTRAINT medication_logs_medicine_id_fkey
FOREIGN KEY (medicine_id)
REFERENCES medicines(id)
ON DELETE CASCADE;

          ALTER TABLE medicine_schedules

DROP CONSTRAINT medicine_schedules_medicine_id_fkey,
ADD CONSTRAINT medicine_schedules_medicine_id_fkey
FOREIGN KEY (medicine_id)
REFERENCES medicines(id)
ON DELETE CASCADE;

        ALTER TABLE patients

DROP CONSTRAINT patients_doctor_id_fkey,
ADD CONSTRAINT patients_doctor_id_fkey
FOREIGN KEY (doctor_id)
REFERENCES doctors(id)
ON DELETE CASCADE;

ALTER TABLE chat_messages
DROP CONSTRAINT chat_messages_receiver_id_fkey,
ADD CONSTRAINT chat_messages_receiver_id_fkey
FOREIGN KEY (receiver_id)
REFERENCES users(id)
ON DELETE CASCADE;

ALTER TABLE chat_messages
DROP CONSTRAINT chat_messages_sender_id_fkey,
ADD CONSTRAINT chat_messages_sender_id_fkey
FOREIGN KEY (sender_id)
REFERENCES users(id)
ON DELETE CASCADE;

    ALTER TABLE doctors

DROP CONSTRAINT doctors_user_id_fkey,
ADD CONSTRAINT doctors_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;

      ALTER TABLE health_trackers

DROP CONSTRAINT health_trackers_user_id_fkey,
ADD CONSTRAINT health_trackers_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;

      ALTER TABLE medicines

DROP CONSTRAINT medicines_user_id_fkey,
ADD CONSTRAINT medicines_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;

      ALTER TABLE patients

DROP CONSTRAINT patients_user_id_fkey,
ADD CONSTRAINT patients_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;
