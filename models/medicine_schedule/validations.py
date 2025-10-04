from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime

class CreateOrUpdateMedicineScheduleValidation(BaseModel):
    # TODO: add other fields validations
    dose: int = Field(ge=1, le=100)
    end_date: Optional[DateTime] = Field(default=None) # TODO: add greater than today midnight validation
