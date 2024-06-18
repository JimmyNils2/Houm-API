from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.property import Property
from db.models.visit import Visit
from pydantic_schemas.property import PropertyCreate, PropertyUpdate


async def get_properties(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        result = await db.execute(select(Property).offset(skip).limit(limit))
        return result.scalars().all()
    except Exception as e:
        raise e


async def get_property(db: AsyncSession, property_id: int):
    try:
        query = select(Property).where(Property.id == property_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        raise e

async def get_property_by_address(db: AsyncSession, address: str):
    try:
        query = select(Property).filter(Property.address == address)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        raise e


async def create_property(db: AsyncSession, property: PropertyCreate):
    try:
        db_property = Property(
            address=property.address,
            location=property.location,
            price=property.price,
            description=property.description,
        )
        db.add(db_property)
        await db.commit()
        await db.refresh(db_property)
        return db_property
    except Exception as e:
        await db.rollback()
        raise e


async def delete_property(db: AsyncSession, property_id: int):
    try:
        query = delete(Visit).where(Visit.property_id == property_id)
        await db.execute(query)
        query = delete(Property).where(Property.id == property_id)
        await db.execute(query)
        await db.commit()
        return {
            "message": f"The property with the id {property_id} deleted successfully"
        }
    except Exception as e:
        await db.rollback()
        raise e


async def update_property(db:AsyncSession, property_id: int, property_update: PropertyUpdate):
    db_property = await get_property(db, property_id)
    if not db_property:
        return None
    
    update_data = property_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_property, key, value)
    
    try:
        await db.commit()
        await db.refresh(db_property)
        return db_property
    except Exception as e:
        await db.rollback()
        raise e