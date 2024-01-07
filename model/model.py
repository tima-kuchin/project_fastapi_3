from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

Base = declarative_base()

# Теги
class Tags(Enum):
    cars = "cars"
    regions = "regions"

# Слой Base для БД
class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    region_name = Column(String, nullable=False)
    region_type = Column(String, nullable=False)
    cars = relationship('Car', back_populates='region')


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    license_plate = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    color = Column(String, nullable=False)
    owner_name = Column(String, nullable=False)
    insurance = Column(Boolean, nullable=False)
    region_id = Column(Integer, ForeignKey('regions.id'))
    region = relationship('Region', back_populates='cars')


# BaseModel для Pydantic
class CarBase(BaseModel):
    license_plate: str|None = None
    brand: str|None = None
    color: str|None = None
    owner_name: str|None = None
    insurance: bool|None = None
    region_id: int|None = None

    model_config = ConfigDict(from_attributes=True)

# Модель для чтения машин
class CarRead(CarBase):
    id: int

# BaseModel для Pydantic для Region
class RegionBase(BaseModel):
    region_name: str|None = None
    region_type: str|None = None

    model_config = ConfigDict(from_attributes=True)

# Модель для чтения региона
class RegionRead(RegionBase):
    id: int

