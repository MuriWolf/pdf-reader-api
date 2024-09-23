from datetime import datetime, timedelta
from http import HTTPStatus
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, DecodeError, encode, ExpiredSignatureError
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from sqlalchemy.orm import session
from src.database import SessionLocal
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


async def get_current_user(
    db: db_dependency,
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get('sub')
        role: str = payload.get('role')
        if not email or not role:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()

    if not user:
        raise credentials_exception
    
    return user

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=ZoneInfo('UTC')) + expires_delta 
    else:
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=15)

    to_encode.update({'exp': expire})
    encoded_jwd = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwd

async def validate_refresh_token(db: db_dependency, refresh_token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get('sub')
        role: str = payload.get('role')
        if not email or not role:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()

    if not user:
        raise credentials_exception
    
    return user, refresh_token 

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

class RoleChecker:
    def __init__(self, allowed_roles) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[models.User, Depends(get_current_user)]):
        if user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não possui permissões suficientes."
        )
