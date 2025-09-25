from pydantic import BaseModel, Field

from models.medicine_schedule.validations import CreateMedicineScheduleValidation

class CreateMedicineValidation(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    form: str = Field() # TODO: validate medicine form as enum
    schedule: CreateMedicineScheduleValidation
