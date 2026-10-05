from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/adopters", tags=["adopters"])

@router.get("/{adopter_id}", response_model = schemas.AdopterOut)
def get_adopter(adopter_id: int, db: Session = Depends(get_db)):
    db_adopter = db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()

    if db_adopter is None:
        raise HTTPException(status_code=404, detail = "Adopter not found")
    return db_adopter

@router.post("", response_model=schemas.AdopterOut, status_code=201)
def create_adopter(adopter: schemas.AdopterCreate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_adopter = models.Adopter(**adopter.model_dump())
    db.add(db_adopter)
    db.commit()
    db.refresh(db_adopter)
    return db_adopter

@router.get("", response_model=list[schemas.AdopterOut])
def list_adopters(db: Session = Depends(get_db)):
    return db.query(models.Adopter).all()


@router.put("/{adopter_id}", response_model=schemas.AdopterOut)
def update_adopter(adopter_id: int, adopter: schemas.AdopterCreate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_adopter = db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()

    if db_adopter is None:
        raise HTTPException(status_code=404, detail="Adopter not found")

    for field, value in adopter.model_dump().items():
        setattr(db_adopter, field, value)

    db.commit()
    db.refresh(db_adopter)
    return db_adopter


@router.delete("/{adopter_id}",status_code=204)
def delete_adopter(adopter_id: int, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_adopter = db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()
    if db_adopter is None:
        raise HTTPException(status_code=404, detail = "Adopter not found")
    
    db.delete(db_adopter)
    db.commit()