from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import get_async_db
from pydantic_schemas.visit import Visit, VisitCreate, VisitUpdate
from db.crud.visitis import (
    get_visits,
    get_visit,
    create_visit,
    delete_visit,
    update_visit,
)
from db.crud.employees import get_employee
from db.crud.properties import get_property

router = APIRouter()


@router.get("/visits", response_model=List[Visit])
async def read_visits(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)
):
    db_visits = await get_visits(db=db, skip=skip, limit=limit)
    return db_visits


@router.get("/visits/{visit_id}", response_model=Visit)
async def read_visit(visit_id: int, db: AsyncSession = Depends(get_async_db)):
    db_visit = await get_visit(db=db, visit_id=visit_id)
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return db_visit


@router.post("/visits", response_model=Visit)
async def create_new_visit(
    visit: VisitCreate, db: AsyncSession = Depends(get_async_db)
):
    db_employee = await get_employee(db=db, employee_id=visit.employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db_property = await get_property(db=db, property_id=visit.property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    return await create_visit(db=db, visit=visit)


@router.delete("/visits/{visit_id}", response_model=dict)
async def remove_visit(visit_id: int, db: AsyncSession = Depends(get_async_db)):
    db_visit = await get_visit(db=db, visit_id=visit_id)
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return await delete_visit(db=db, visit_id=visit_id)


@router.patch("/visits/{visit_id}", response_model=Visit)
async def patch_visit(
    visit_id: int, visit_update: VisitUpdate, db: AsyncSession = Depends(get_async_db)
):

    db_visit = await update_visit(
      db=db, visit_id=visit_id, visit_update=visit_update
    )
    if db_visit is None:
        raise HTTPException(status_code=404, detail="Visit not found")
    return db_visit
