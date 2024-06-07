from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Fine_content(BaseModel):
    name: str
    lastModified: int
    text: str

class Traffic_violation(BaseModel):
    id: int
    id_user: int
    nome_do_condutor: str
    nome_pessoa: str
    cpf: str
    placa_veiculo: str
    infracao: str
    gravidade: str
    data_infracao: str # verificar o TYPE
    hora_infracao: str # verificar o TYPE
    endereco_infracao: str

class User(BaseModel):
    id: int
    name: str
    emai: str

@app.post("/fines")
async def post_fine_text(fine_text: List[Fine_content]):
    return { "msg": "sucess", "code": 200 }

@app.get("/fines/{fine_id}")
async def get_fine(fine_id: int):

    # do logic to communicate with the backend
    fine: Traffic_violation = {
        "id": 12345,
        "id_user": 1,
        "nome_do_condutor": "João Silva",
        "nome_pessoa": "Maria Santos",
        "cpf": "123.456.789-00",
        "placa_veiculo": "ABC-1234",
        "infracao": "Excesso de velocidade",
        "gravidade": "Grave",
        "data_infracao": "2024-05-15",
        "hora_infracao": "10:30:00",
        "endereco_infracao": "Rua das Flores, 123 - Centro, São Paulo/SP"
    }
    return fine

@app.get("/fines")
async def get_fines(id_user: int | None = None):
    # do logic to communicate with the backend
    fine: Traffic_violation = {
        "id": 12345,
        "id_user": 1,
        "nome_do_condutor": "João Silva",
        "nome_pessoa": "Maria Santos",
        "cpf": "123.456.789-00",
        "placa_veiculo": "ABC-1234",
        "infracao": "Excesso de velocidade",
        "gravidade": "Grave",
        "data_infracao": "2024-05-15",
        "hora_infracao": "10:30:00",
        "endereco_infracao": "Rua das Flores, 123 - Centro, São Paulo/SP"
    }

    if (id_user):
        pass
    else:
        pass

    fines = [fine, fine, fine, fine]

    return fines

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user: User = { 
        "id": user_id,
        "name": "Murillo",
        "email": "email@gmail.com",
        "quantidade_posts": 3 
    }

    return user