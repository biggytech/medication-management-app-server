from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from models.common.enums.sex_types import SexTypes


class SignInDefaultValidation(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class CreateUserValidation(SignInDefaultValidation):
    full_name: str = Field(min_length=1, max_length=255)


class UpdateUserValidation(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    sex: Optional[SexTypes] = None
    # date_of_birth: Optional[date] = None
