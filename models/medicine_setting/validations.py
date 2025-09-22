from pydantic import BaseModel, Field

class CreateMedicineSettingValidation(BaseModel):
    dose: int = Field(ge=1, le=100)
