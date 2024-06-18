from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import get_async_db
from pydantic_schemas.property import Property, PropertyCreate, PropertyUpdate
from db.crud.properties import (
    get_properties,
    get_property,
    create_property,
    get_property_by_address,
    delete_property,
    update_property
)

router = APIRouter()


@router.get("/properties", response_model=List[Property])
async def read_properties(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)
):
    db_properties = await get_properties(db=db, skip=skip, limit=limit)
    return db_properties


@router.get("/properties/{property_id}", response_model=Property)
async def read_property(property_id: int, db: AsyncSession = Depends(get_async_db)):
    db_property = await get_property(db=db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property


@router.post("/properties", response_model=Property)
async def create_new_property(
    property: PropertyCreate, db: AsyncSession = Depends(get_async_db)
):
    db_property = await get_property_by_address(db=db, address=property.address)
    if db_property:
        raise HTTPException(status_code=400, detail="Address is already registered")
    return await create_property(db=db, property=property)


@router.delete("/properties/{property_id}", response_model=dict)
async def remove_property(property_id: int, db: AsyncSession = Depends(get_async_db)):
    db_property = await get_property(db=db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return await delete_property(db=db, property_id=property_id)


@router.patch("/properties/{property_id}", response_model=Property)
async def patch_property(
    property_id: int,
    property_update: PropertyUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    db_property = await update_property(
        db=db, property_id=property_id, property_update=property_update
    )
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property
