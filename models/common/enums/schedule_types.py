import enum

from sqlalchemy.dialects.postgresql import ENUM as pgEnum

from models.base import Base


class ScheduleTypes(str, enum.Enum):
    every_day = "every_day"
    every_other_day = "every_other_day"
    every_x_days = "every_x_days"
    specific_week_days = "specific_week_days"
    only_as_needed = "only_as_needed"


ScheduleTypesType: pgEnum = pgEnum(
    ScheduleTypes,
    name="schedule_types",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True
)
