from datetime import datetime
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models.visit import Visit
from pydantic_schemas.visit import VisitCreate, VisitUpdate


async def get_visits(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        result = await db.execute(select(Visit).offset(skip).limit(limit))
        return result.scalars().all()
    except Exception as e:
        raise e

async def get_visit(db: AsyncSession, visit_id: int):
    try:
        query = select(Visit).where(Visit.id == visit_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        raise e


async def create_visit(db: AsyncSession, visit: VisitCreate):
    try:
        db_visit = Visit(**visit.dict())
        db.add(db_visit)
        await db.commit()
        await db.refresh(db_visit)
        return db_visit
    except Exception as e:
        await db.rollback()
        raise e


async def delete_visit(db: AsyncSession, visit_id: int):
  try:
    query = delete(Visit).where(Visit.id == visit_id)
    await db.execute(query)
    await db.commit()
    return {"message": f"The visit with the id {visit_id} deleted successfully"}
  except Exception as e:
    await db.rollback()
    raise e


async def update_visit(db: AsyncSession, visit_id: int, visit_update: VisitUpdate):
    db_visit = await get_visit(db, visit_id)
    if not db_visit:
        return None
    
    update_data = visit_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_visit, key, value)
    
    try:
        await db.commit()
        await db.refresh(db_visit)
        return db_visit
    except Exception as e:
        await db.rollback()
        raise e
