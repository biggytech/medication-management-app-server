from typing import Optional

from pydantic import BaseModel, Field
from pydantic_extra_types.pendulum_dt import DateTime


class AddHealthTrackerLogValidation(BaseModel):
    date: DateTime = Field()  # TODO: add greater than today midnight validation
    value1: float = Field()
    value2: Optional[float] = Field(default=None)
