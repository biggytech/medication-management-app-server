from pydantic import BaseModel, Field

from models.medicine_setting.validations import CreateMedicineSettingValidation

class CreateMedicineValidation(BaseModel):
    # TODO: validate medicine form
    title: str = Field(min_length=1, max_length=255)
    setting: CreateMedicineSettingValidation
