from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal, Base

# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pet Catalog API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message":"Pet catalog API works"}


@app.post("/animals", response_model=schemas.AnimalOut, status_code=201)
def create_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    db_animal = models.Animal(**animal.model_dump())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


@app.get("/animals/{animal_id}", response_model =schemas.AnimalOut)
def get_amimal(animal_id: int, db: Session = Depends(get_db)):
    db_animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()

    if db_animal is None:
        raise HTTPException(status_code=404, detail = "Animal not found")
    return db_animal


@app.get("/animals", response_model=list[schemas.AnimalOut])
def list_animals(species: Optional[str] = None,
                 breed: Optional[str] = None,
                 status: Optional[str] = None,
                 age_min :Optional[int] = None,
                 age_max: Optional[int] = None,
                 skip:int = 0,
                 limit: int = 20,
                 db: Session = Depends(get_db)):
    
    query = db.query(models.Animal)

    if species:
        query = query.filter(models.Animal.species == species)
    if breed:
        query = query.filter(models.Animal.breed.ilike(f"%{breed}%"))
    if status:
        query = query.filter(models.Animal.status == status)
    if age_min is not None:
        query = query.filter(models.Animal.age >= age_min)
    if age_max is not None:
        query = query.filter(models.Animal.age <= age_max)
    
    return query.offset(skip).limit(limit).all()


@app.put("/animals/{animal_id}", response_model = schemas.AnimalOut)
def update_animal(animal_id: int,animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    db_animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if db_animal is None:
        raise HTTPException(status_code=404, detail = "Animal not found")
    

    for field, value in animal.model_dump().items():
        setattr(db_animal, field, value)

    db.commit()
    db.refresh(db_animal)
    return db_animal
    

@app.delete("/animals/{animal_id}", status_code=204)
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    db_animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if db_animal is None:
        raise HTTPException(status_code=404, detail = "Animal not found")
    
    db.delete(db_animal)
    db.commit()


@app.get("/adopters/{adopter_id}", response_model = schemas.AdopterOut)
def get_adopter(adopter_id: int, db: Session = Depends(get_db)):
    db_adopter = db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()

    if db_adopter is None:
        raise HTTPException(status_code=404, detail = "Animal not found")
    return db_adopter

@app.post("/adopters", response_model=schemas.AdopterOut, status_code=201)
def create_adopter(adopter: schemas.AdopterCreate, db: Session = Depends(get_db)):
    db_adopter = models.Adopter(**adopter.model_dump())
    db.add(db_adopter)
    db.commit()
    db.refresh(db_adopter)
    return db_adopter

@app.get("/adopters", response_model=list[schemas.AdopterOut])
def list_adopters(db: Session = Depends(get_db)):
    return db.query(models.Adopter).all()


@app.put("/adopters/{adopter_id}", response_model=schemas.AdopterOut)
def update_adopter(adopter_id: int, adopter: schemas.AdopterCreate, db: Session = Depends(get_db)):
    db_adopter = db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()

    if db_adopter is None:
        raise HTTPException(status_code=404, detail="Adopter not found")

    for field, value in adopter.model_dump().items():
        setattr(db_adopter, field, value)

    db.commit()
    db.refresh(db_adopter)
    return db_adopter


@app.delete("/adopters/{adopter_id}",status_code=204)
def delete_adopter(adopter_id: int, db: Session = Depends(get_db)):
    db_adopter = db.query(models.Adopter).filter(models.Adopter.id == adopter_id).first()
    if db_adopter is None:
        raise HTTPException(status_code=404, detail = "Adopter not found")
    
    db.delete(db_adopter)
    db.commit()


@app.post("/adoptions", response_model = schemas.AdoptionOut, status_code=201)
def create_adoption(adoption: schemas.AdoptionCreate, db: Session = Depends(get_db)):
    db_animal = db.query(models.Animal).filter(models.Animal.id == adoption.animal_id).first()

    if db_animal is None:
        raise HTTPException(status_code=404, detail = "Adopter not found")
    
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
