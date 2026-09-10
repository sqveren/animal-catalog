from sqlalchemy import Column, Integer, String, MetaData, Date
from app.database import Base


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    status = Column(String, default="available",nullable=False)
    arrival_date = Column(Date, nullable=False)
    description = Column(String, nullable=True)
    