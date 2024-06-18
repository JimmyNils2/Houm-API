from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class PropertyBase(BaseModel):
    address: str
    location: str
    price: Optional[Decimal]
    description: Optional[str]


class PropertyCreate(PropertyBase):
    price: Decimal = Field(..., description="The price of the property", example=100000.0)
    description: str = Field(None, description="The description of the property", example="Beautiful house in a quiet neighborhood")

class Property(PropertyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PropertyUpdate(BaseModel):
    address: Optional[str] = Field(None, description="The property's address")
    location: Optional[str] = Field(None, description="The property's location")
    price: Optional[Decimal] = Field(None, description="The property's price")
    description: Optional[str] = Field(None, description="The property's description")

    class Config:
        orm_mode = True
