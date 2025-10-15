from typing import Optional

from pydantic import BaseModel, Field


class UpdateDoctorValidation(BaseModel):
    """Validation schema for updating an existing doctor."""
    specialisation: Optional[str] = Field(None, min_length=1, max_length=255,
                                          description="Doctor's medical specialisation")
    place_of_work: Optional[str] = Field(None, min_length=1, max_length=255, description="Place where the doctor works")
    photo_url: Optional[str] = Field(None, max_length=500, description="Local file path for doctor's photo")


class CreateDoctorValidation(UpdateDoctorValidation):
    """Validation schema for creating a new doctor."""
    user_id: int = Field(gt=0, description="ID of the user account linked to this doctor")

