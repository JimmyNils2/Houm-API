from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class EmployeeBase(BaseModel):
    email: str
    name: str


class EmployeeCreate(EmployeeBase): ...


class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attibutes = True

class EmployeeUpdate(BaseModel):
    email: Optional[str] = Field(None, description="The employee's email")
    name: Optional[str] = Field(None, description="The employee's name")

    class ConfigDict:
        from_attibutes = True
