import enum

from sqlalchemy.dialects.postgresql import ENUM as pgEnum

from models.base import Base


class SexTypes(str, enum.Enum):
    male = "male"
    female = "female"


SexTypesType: pgEnum = pgEnum(
    SexTypes,
    name="sex_types",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True
)
