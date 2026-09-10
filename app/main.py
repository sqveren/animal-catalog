from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

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
def get_all_animals(db: Session = Depends(get_db)):
    db_animals = db.query(models.Animal).all()
    
    return db_animals

@app.put("/animal/{animal_id}", response_model = schemas.AnimalOut)
def update_animal(animal_id: int,animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    db_animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if db_animal is None:
        raise HTTPException(status_code=404, detail = "Animal not found")
    

    for field, value in animal.model_dump().items():
        setattr(db_animal, field, value)

    db.refresh(db_animal)
    return db_animal
    

@app.delete("/animal/{animal_id}", status_code=204)
def delete_animal(animal_id: int, db: Session = Depends(get_db)):
    db_animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if db_animal is None:
        raise HTTPException(status_code=404, detail = "Animal not found")
    
    db.delete(db_animal)
    db.commit()


