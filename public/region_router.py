from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db_engine import get_async_session
from model.model import Tags, Region, RegionRead, RegionBase

region_router = APIRouter(prefix='/api/regions', tags=[Tags.regions])


@region_router.get("/{region_id}", response_model=RegionRead, tags=[Tags.regions])
async def read_region(region_id: int, db: AsyncSession = Depends(get_async_session)):
    statement = select(Region).where(Region.id == region_id)
    region = await db.scalar(statement)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return RegionRead.model_validate(region)


@region_router.get("/", response_model=list[RegionRead], tags=[Tags.regions])
async def read_regions(db: AsyncSession = Depends(get_async_session)):
    statement = select(Region)
    regions = await db.scalars(statement)
    if regions is None:
        raise HTTPException(status_code=404, detail="Regions not found")
    return [RegionRead.model_validate(region) for region in regions]


@region_router.post("/", response_model=RegionRead, tags=[Tags.regions])
async def create_region(region: RegionBase, db: AsyncSession = Depends(get_async_session)):
    # Если данные не прошли валидацию, генерируем ошибку
    if region.model_dump(exclude_none=True) != region.model_dump():
        raise HTTPException(status_code=400, detail="Have NULL fields")

    new_region = Region(**region.model_dump())

    db.add(new_region)
    await db.commit()
    await db.refresh(new_region)
    return RegionRead.model_validate(new_region)


@region_router.delete("/{region_id}", response_model=RegionRead, tags=[Tags.regions])
async def delete_region(region_id: int, db: AsyncSession = Depends(get_async_session)):
    statement = select(Region).where(Region.id == region_id)
    region = await db.scalar(statement)
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    await db.delete(region)
    await db.commit()
    return Response(status_code=204)