from pydantic import BaseModel, Field, EmailStr

class SignInDefaultValidation(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class CreateUserValidation(SignInDefaultValidation):
    full_name: str = Field(min_length=1, max_length=255)
