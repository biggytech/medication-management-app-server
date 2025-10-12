from typing import Optional

from pydantic import BaseModel, Field

from models.health_tracker_schedule.validations import CreateOrUpdateHealthTrackerScheduleValidation


class CreateOrUpdateHealthTrackerValidation(BaseModel):
    type: str = Field()  # TODO: validate type as enum
    schedule: CreateOrUpdateHealthTrackerScheduleValidation
    notes: Optional[str] = Field(min_length=0, max_length=255, default=None)
