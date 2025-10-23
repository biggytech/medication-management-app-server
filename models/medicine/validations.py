from typing import Optional

from pydantic import BaseModel, Field

from models.medicine_schedule.validations import CreateOrUpdateMedicineScheduleValidation


class CreateOrUpdateMedicineValidation(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    form: str = Field()  # TODO: validate medicine form as enum
    schedule: CreateOrUpdateMedicineScheduleValidation
    notes: Optional[str] = Field(min_length=0, max_length=255, default=None)
    # count: int = Field(ge=1, le=9999, default=None)  # TODO: add counts validations (min=1, max
