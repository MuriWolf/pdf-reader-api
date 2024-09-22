from src.schemas import UserPublic
from src.models import User

def convert_user_to_public(user: User) -> UserPublic:
    return UserPublic(
       id=user.id_user,
       nome_user=user.nome_user,
       foto=user.foto,
       email=user.email,
       role=user.role,
       username=user.username
    )
