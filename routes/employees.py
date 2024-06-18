from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import get_async_db
from pydantic_schemas.employee import Employee, EmployeeCreate, EmployeeUpdate
from pydantic_schemas.visit import Visit
from db.crud.employees import (
    create_employee,
    get_employee_by_email,
    get_employees,
    get_employee,
    get_employee_visits,
    delete_employee,
    update_employee,
)

router = APIRouter()


@router.get("/employees", response_model=List[Employee])
async def read_employees(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)
):
    db_employees = await get_employees(db=db, skip=skip, limit=limit)
    return db_employees


@router.get("/employees/{employee_id}", response_model=Employee)
async def read_employee(employee_id: int, db: AsyncSession = Depends(get_async_db)):
    db_employee = await get_employee(db=db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.post("/employees", response_model=Employee)
async def create_new_employee(
    employee: EmployeeCreate, db: AsyncSession = Depends(get_async_db)
):
    db_employee = await get_employee_by_email(db=db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return await create_employee(db=db, employee=employee)


@router.delete("/employees/{employee_id}", response_model=dict)
async def remove_employee(employee_id: int, db: AsyncSession = Depends(get_async_db)):
    db_employee = await get_employee(db=db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return await delete_employee(db=db, employee_id=employee_id)


@router.patch("/employees/{employee_id}", response_model=Employee)
async def patch_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    db_employee = await update_employee(
        db=db, employee_id=employee_id, employee_update=employee_update
    )
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.get("/employees/{employee_id}/report", response_model=dict)
async def read_report(employee_id: int, db: AsyncSession = Depends(get_async_db)):
    visits, total = await get_employee_visits(db=db, employee_id=employee_id)

    if not visits:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {
        "total_properties": total,
        "total_km": "TODO"
    }
