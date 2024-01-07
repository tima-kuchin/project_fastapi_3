from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db_engine import get_async_session
from model.model import Car, CarRead, Tags, CarBase, Region

car_router = APIRouter(prefix='/api/cars', tags=[Tags.cars])


@car_router.get("/{car_id}", response_model=CarRead, tags=[Tags.cars])
async def read_car(car_id: int, db: AsyncSession = Depends(get_async_session)):
    statement = select(Car).where(Car.id == car_id)
    car = await db.scalar(statement)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return CarRead.model_validate(car)


@car_router.get("/", response_model=list[CarRead], tags=[Tags.cars])
async def read_cars(db: AsyncSession = Depends(get_async_session)):
    statement = select(Car)
    cars = await db.scalars(statement)
    if cars is None:
        raise HTTPException(status_code=404, detail="Cars not found")
    return [CarRead.model_validate(car) for car in cars]


@car_router.post("/", response_model=CarRead, tags=[Tags.cars])
async def create_car(car: CarBase, db: AsyncSession = Depends(get_async_session)):
    # Если данные не прошли валидацию, генерируем ошибку
    if car.model_dump(exclude_none=True) != car.model_dump():
        raise HTTPException(status_code=400, detail="Have NULL fields")

    # Проверка наличия региона в таблице регионов
    region =  await db.scalar(select(Region).where(Region.id == car.region_id))
    if not region:
        raise HTTPException(status_code=404, detail="Region not founds")

    new_car = Car(**car.model_dump())

    db.add(new_car)
    await db.commit()
    await db.refresh(new_car)
    return CarRead.model_validate(new_car)


@car_router.patch("/{car_id}", response_model=CarRead, tags=[Tags.cars])
async def patch_car(car_id: int, updated_car: CarBase, db: AsyncSession = Depends(get_async_session)):
    statement = select(Car).where(Car.id == car_id)
    car = await db.scalar(statement)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    for field, value in updated_car.model_dump(exclude_unset=True).items():
        setattr(car, field, value)

    await db.commit()
    await db.refresh(car)
    return CarRead.model_validate(car)


@car_router.put("/{car_id}", response_model=CarRead, tags=[Tags.cars])
async def update_car(car_id: int, updated_car: CarBase, db: AsyncSession = Depends(get_async_session)):
    if updated_car.model_dump(exclude_none=True) != updated_car.model_dump():
        raise HTTPException(status_code=400, detail="Have NULL fields")

    statement = select(Car).where(Car.id == car_id)
    car = await db.scalar(statement)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    for field, value in updated_car.model_dump().items():
        setattr(car, field, value)

    await db.commit()
    await db.refresh(car)
    return CarRead.model_validate(car)


@car_router.delete("/{car_id}", response_model=CarRead, tags=[Tags.cars])
async def delete_car(car_id: int, db: AsyncSession = Depends(get_async_session)):
    statement = select(Car).where(Car.id == car_id)
    car = await db.scalar(statement)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    await db.delete(car)
    await db.commit()
    return Response(status_code=204)