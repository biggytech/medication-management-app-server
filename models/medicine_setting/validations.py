from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime

class CreateMedicineSettingValidation(BaseModel):
    dose: int = Field(ge=1, le=100)
    end_date: Optional[DateTime] = Field() # TODO: add greater than today midnight validation
