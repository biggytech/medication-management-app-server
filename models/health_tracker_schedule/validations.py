from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime


class CreateOrUpdateHealthTrackerScheduleValidation(BaseModel):
    # TODO: add other fields validations
    # type
    every_x_days: int = Field(ge=0, le=365)
    # notification_times
    user_time_zone: str = Field(min_length=1, max_length=255)
    next_take_date: Optional[DateTime] = Field(default=None)  # TODO: add greater than today midnight validation
    # days_of_week
    end_date: Optional[DateTime] = Field(default=None)  # TODO: add greater than today midnight validation
