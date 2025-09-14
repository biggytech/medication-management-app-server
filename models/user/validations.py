from pydantic import BaseModel, PositiveInt, ValidationError, Field, EmailStr

class CreateUserValidation(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8)
