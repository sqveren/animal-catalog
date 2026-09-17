from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date, Float, func
from sqlalchemy.orm import relationship


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
    weight = Column(Float, nullable=True)

    adoptions = relationship("Adoption", back_populates="animal")

    

class Adopter(Base):
    __tablename__ = "adopters"

    id = Column(Integer, primary_key=True, index = True)
    first_name = Column(String, nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=True)
    registered_at = Column(DateTime, server_default=func.now())

    adoptions = relationship("Adoption", back_populates="adopter")

class Adoption(Base):
    __tablename__ = "adoptions"

    id = Column(Integer, primary_key=True, index = True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    adopter_id = Column(Integer,ForeignKey("adopters.id"),nullable=False)
    adoption_time = Column(DateTime, server_default=func.now())
    status = Column(String, default="pending", nullable=False)

    animal = relationship("Animal", back_populates="adoptions")
    adopter = relationship("Adopter", back_populates="adoptions")


