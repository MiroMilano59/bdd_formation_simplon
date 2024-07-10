from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from BDD import schemas, models, crud, get_db


app = FastAPI()

# Dependency
def get_db():
    db = get_db() # SessionLocal
    try:
        # utiliser yield pour exécuter des étapes en plus
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"message": "Hello API Formation Simplon"}


# /formation/{formaCode} exemple de route pour récupérer une formation avec un formaCode
@app.get("/formation")
def get_formation(item:schemas.Item, db:Session = Depends(get_db)):
    elements = crud.get_formation(db=db, formacode = item.formaCode)
    return elements