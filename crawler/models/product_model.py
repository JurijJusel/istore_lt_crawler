from __future__ import annotations
from pydantic import BaseModel, field_validator


class IstoreItemModel(BaseModel):
    name: str
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
