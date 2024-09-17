from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Annotated
import src.sql_app.models as models
from src.sql_app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from src.functions import LeitorFinal
from src.schemas import UserBase, PdfContentBase, TrafficViolationBase 
 
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/fines", status_code=status.HTTP_201_CREATED)
async def post_fine_data(fines_data: List[PdfContentBase], db: db_dependency):
    for fine in fines_data: 
        fine_values = LeitorFinal.main(fine.text)
        # return fine_values
        db_fine = models.PDF(**fine_values, user_id=fine.userId, 
        data_envio=fine.dataEnvio)
        db.add(db_fine)
        db.commit()
        db.refresh(db_fine)
    return { "code": 200, "msg": "success" }

@app.get("/fines", status_code=status.HTTP_200_OK)
async def get_fines(db: db_dependency, id_user: int | None = None, username: str | None = None):
    fines = []
    if (id_user):
        fines = db.query(models.PDF).filter(models.PDF.user_id == id_user).all()
    elif (username):
        user = db.query(models.User).filter(models.User.username == username).first()
        if (user):
            fines = db.query(models.PDF).filter(models.PDF.user_id == user.id_user).all()
        else:
            raise HTTPException(status_code=404, detail='Usuario não encontrado')
    else:
        fines = db.query(models.PDF).all()

    if (len(fines) == 0):
        raise HTTPException(status_code=404, detail='Nenhum documento foi encontrado')
    return fines

@app.get("/users", status_code=status.HTTP_200_OK)      
async def get_user(db: db_dependency, user_id: int | None = None, username: str | None = None):
    user = None
    if (user_id):
        user = db.query(models.User).filter(models.User.id_user == user_id).first()
    elif (username):
        user = db.query(models.User).filter(models.User.username == username).first()
    else:
        user = db.query(models.User).all()
    
    if user is None:
        raise HTTPException(status_code=404, detail='Usuario não encontrado')
    
    return user
        

