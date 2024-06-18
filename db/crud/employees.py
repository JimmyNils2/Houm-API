from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.employee import Employee
from db.models.visit import Visit
from pydantic_schemas.employee import EmployeeCreate, EmployeeUpdate


async def get_employees(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        result = await db.execute(select(Employee).offset(skip).limit(limit))
        return result.scalars().all()
    except Exception as e:
        raise e


async def get_employee(db: AsyncSession, employee_id: int):
    try:
        query = select(Employee).where(Employee.id == employee_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        raise e


async def get_employee_visits(db: AsyncSession, employee_id: int):
    try:
        result = await db.execute(
            select(Visit)
            .filter(Visit.employee_id == employee_id)
        )
        visits = result.scalars().all()
        return visits, len(visits)
    except Exception as e:
        raise e


async def get_employee_report(db: AsyncSession, employee_id: int):
    try:
        visits = await get_employee_visits(db=db, employee_id=employee_id)

        if visits:
            # TODO How to calculate total distance traveled?
            return {
                "employee_id": employee_id,
                "properties_visited": visits
            }
    except Exception as e:
        raise e


async def get_employee_by_email(db: AsyncSession, email: str):
    try:
        query = select(Employee).filter(Employee.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        raise e


async def create_employee(db: AsyncSession, employee: EmployeeCreate):
    try:
        db_employee = Employee(email=employee.email, name=employee.name)
        db.add(db_employee)
        await db.commit()
        await db.refresh(db_employee)
        return db_employee
    except Exception as e:
        await db.rollback()
        raise e


async def delete_employee(db: AsyncSession, employee_id: int):
    try:
        query = delete(Visit).where(Visit.employee_id == employee_id)
        await db.execute(query)
        query = delete(Employee).where(Employee.id == employee_id)
        await db.execute(query)
        await db.commit()
        return {
            "message": f"The employee with the id {employee_id} deleted successfully"
        }
    except Exception as e:
        await db.rollback()
        raise e


async def update_employee(
    db: AsyncSession, employee_id: int, employee_update: EmployeeUpdate
):
    db_employee = await get_employee(db, employee_id)
    if not db_employee:
        return None

    update_data = employee_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)

    try:
        await db.commit()
        await db.refresh(db_employee)
        return db_employee
    except Exception as e:
        await db.rollback()
        raise e
