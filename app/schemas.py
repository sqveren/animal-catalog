from pydantic import BaseModel
from datetime import date
from typing import Optional


class AnimalCreate(BaseModel):
    name: str
    species:  str
    breed: Optional[str] = None
    age: Optional[int] = None
    arrival_date: date
    description: Optional[str] = None


class AnimalOut(AnimalCreate):
    id: int
    status: str

    class Config:
        from_attributes = True