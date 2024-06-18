from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class VisitBase(BaseModel):
    visit_date: datetime
    comment: Optional[str]


class VisitCreate(VisitBase):
    employee_id: int
    property_id: int


class Visit(VisitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    employee_id: int
    property_id: int

    class Config:
        orm_mode = True


class VisitUpdate(BaseModel):
    visit_date: Optional[datetime]
    comment: Optional[str]

    class Config:
        orm_mode = True
