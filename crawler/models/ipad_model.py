from pydantic import field_validator
from models.base_model import BaseItemModel

class IpadItemModel(BaseItemModel):
    params: str


    @field_validator('name')
    def clean_name(cls, v):
        return v.strip()

    @field_validator('params')
    def clean_params(cls, v):
        return v.strip()
