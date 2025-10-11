from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime


class TakeMedicationLogValidation(BaseModel):
    date: DateTime = Field()  # TODO: add greater than today midnight validation


class SkipMedicationLogValidation(TakeMedicationLogValidation):
    skip_reason: str = Field()  # TODO: validate skip_reason as enum
