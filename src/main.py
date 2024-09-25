from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Annotated
import src.models as models
from src.database import engine, SessionLocal
from sqlalchemy.orm import Session
from src.functions import leitor_final
from src.schemas import UserBase, UserPublic, UserUpdate, PdfContentBase, TrafficViolationBase, Token, UserLogin, MessageResponse, TokenData 
from src.security import get_password_hash, verify_password, create_token, get_current_user, validate_refresh_token
from src.utils import convert_user_to_public, is_update_from_commom_user_valid
from datetime import timedelta
from src.settings import Settings

settings = Settings()

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
        fine_values = leitor_final.main(fine.text)
        # return fine_values
        db_fine = models.PDF(**fine_values, user_id=fine.userId, data_envio=fine.dataEnvio)
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
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado.')
    else:
        fines = db.query(models.PDF).all()

    if (len(fines) == 0):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Nenhum documento foi encontrado.')
    return fines

@app.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, user: UserBase):
    db_user = db.query(models.User).filter(models.User.username == user.username or models.User.email == user.email).first()

    if (db_user):
        if (db_user.username == user.username):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username já existe.'
            )
        elif (db_user.email == user.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email já existe.'
            )
        
    hashed_password = get_password_hash(user.senha)
    db_user = models.User(
        username=user.username,
        email=user.email,
        nome_user=user.nome_user,
        senha=hashed_password, 
        role=user.role,
        foto=''
    )

    db.add(db_user)    
    db.commit()
    db.refresh(db_user)

    response_user = convert_user_to_public(db_user)
    return response_user

@app.get("/users", status_code=status.HTTP_200_OK)      
async def get_user(db: db_dependency, user_id: int | None = None, username: str | None = None, email: str | None = None):
    user = None
    users = None
    if (user_id):
        user = db.query(models.User).filter(models.User.id_user == user_id).first()
    elif (email):
        user = db.query(models.User).filter(models.User.email == email).first()
    elif (username):
        user = db.query(models.User).filter(models.User.username == username).first()
    else:
        users = db.query(models.User).all()
        users = [convert_user_to_public(u) for u in users]
    
    if user is None and users is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado.')
    elif user is None:
        return users
    else:
        return convert_user_to_public(user)

@app.get("/users/me", response_model=UserPublic, status_code=status.HTTP_200_OK)
def read_users_me(
        db: db_dependency,
        current_user: models.User = Depends(get_current_user)
    ):
    return convert_user_to_public(current_user)

@app.patch('/users/{user_id}', response_model=UserPublic, status_code=status.HTTP_200_OK) 
def update_user(
    db: db_dependency,
    user_id: int,
    user: UserUpdate,
    current_user: models.User = Depends(get_current_user)
):
    user_valid_update = is_update_from_commom_user_valid(user=user, attrs_allowed=["foto"]) 

    if (current_user.role.value != "admin"):
        if (current_user.id_user != user_id or not user_valid_update):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Sem permissões suficientes'
            )

    db_user = db.query(models.User).filter(models.User.id_user == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuario não encontrado'
        )

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    response_user = convert_user_to_public(db_user)

    return response_user 

@app.delete("/users/{user_id}", response_model=MessageResponse)
def delete_user(
    db: db_dependency,
    user_id: int,
    current_user: models.User = Depends(get_current_user)
):
    if (current_user.role.value != "admin"):
        if (current_user.id_user != user_id):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Sem permissões suficientes'
            )

    db_user = db.query(models.User).filter(models.User.id_user == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuario não encontrado" 
        )

    db.delete(db_user)
    db.commit()

    return {'code': HTTPStatus.OK, 'msg': 'Usuario deletado'}

@app.post("/token", response_model=Token)
def login_for_access_token(
    db: db_dependency,
    form_data: UserLogin
):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email ou usuario incorreto"
        )
    
    if not verify_password(form_data.senha, user.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email ou usuario incorreto"
        ) 
    
    access_token = create_token(data={ 'sub': user.email, 'role': user.role.value }, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token(data={ 'sub': user.email, 'role': user.role.value }, expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}

@app.post("logout")
async def logout(token: Token):
    # revoked_tokens.add(token)
    return { "code": 200, "message": "Deslogado com sucesso" }

@app.post("/refresh", response_model=Token)
def refresh_access_token(
    token_data: Annotated[tuple[models.User, str], Depends(validate_refresh_token)]
):
    user, refresh_token = token_data
    new_access_token = create_token(data={'sub': user.email, 'role': user.role.value}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    return {'access_token': new_access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}
