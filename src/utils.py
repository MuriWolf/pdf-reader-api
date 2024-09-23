from src.schemas import UserPublic, UserUpdate
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

def is_update_from_commom_user_valid(user: UserUpdate, attrs_allowed: list[str]):
   for attr, value in user.__dict__.items():
      # Neste caso, tanto faz se possui valor ou não, pois é um atributo que o usuário comum é permitido alterar.
      if attr in attrs_allowed:
         continue
      else:
         if value != None:
            return False
   return True