from fastapi import FastAPI
from app.routers import animals, adopters, adoptions, auth

app = FastAPI(title="Pet Catalog API")

app.include_router(auth.router)
app.include_router(animals.router)
app.include_router(adopters.router)
app.include_router(adoptions.router)


@app.get("/")
def read_root():
    return {"message": "Pet catalog API works"}