from __future__ import annotations
from pydantic import BaseModel, field_validator


class IpadItemModel(BaseModel):
    name: str
    params: str
    price: str
    downloaded_date: str
    availability: str
    url: str
    image_url: str

    @field_validator('price')
    def clean_price(cls, v):
        return v.replace('\xa0', '').replace('€', '').replace(' ', '').strip()

    @field_validator('availability')
    def clean_availability(cls, v):
        return v.strip().lower()

    @field_validator('name')
    def clean_name(cls, v):
        return v.strip()

    @field_validator('params')
    def clean_params(cls, v):
        return v.strip()
