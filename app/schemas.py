from pydantic import BaseModel
from datetime import date
from typing import Optional
from datetime import datetime


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


class AdopterCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None


class AdopterOut(AdopterCreate):
    id: int
    registered_at: datetime

    class Config:
        from_attributes = True

class AdoptionCreate(BaseModel):
    animal_id: int
    adopter_id: int

class AdoptionOut(AdoptionCreate):
    id: int
    adoption_time: datetime
    status:str

    class Config:
        from_attributes = True
    

