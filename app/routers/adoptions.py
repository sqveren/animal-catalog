from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/adoptions", tags=["adoptions"])



@router.post("", response_model = schemas.AdoptionOut, status_code=201)
def create_adoption(adoption: schemas.AdoptionCreate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_animal = db.query(models.Animal).filter(models.Animal.id == adoption.animal_id).first()

    if db_animal is None:
        raise HTTPException(status_code=404, detail = "Animal not found")
    
    if db_animal.status != "available":
        raise HTTPException(status_code=400, detail = "Animal is not available")
    
    db_adopter = db.query(models.Adopter).filter(models.Adopter.id == adoption.adopter_id).first()
    if db_adopter is None:
        raise HTTPException(status_code=404, detail="Adopter not found")

    db_adoption = models.Adoption(animal_id=adoption.animal_id, adopter_id=adoption.adopter_id)
    db.add(db_adoption)

    db_animal.status = "pending"

    db.commit()
    db.refresh(db_adoption)
    return db_adoption