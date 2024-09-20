from datetime import datetime, timedelta
from http import HTTPStatus
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, DecodeError, encode, ExpiredSignatureError
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from sqlalchemy.orm import session
from src.database import engine, SessionLocal
from src.schemas import TokenData
import src.models as models
from sqlalchemy.orm import Session
from typing import List, Annotated
from src.settings import Settings

settings = Settings()

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def get_current_user(
    db: db_dependency,
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == token_data.username).first()

    if not user:
        raise credentials_exception
    
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwd = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwd

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)