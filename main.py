from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Fine_content(BaseModel):
    content: str

class Traffic_violation(BaseModel):
    nome_do_condutor: str
    cpf: str
    placa_do_veiculo: str
    modelo_do_veiculo: str
    marca_do_veiculo: str
    data_e_hora_da_infracao: str
    local_da_infracao: str
    tipo_de_infracao: str
    valor_da_multa: str
    ponto_de_referencia: str
    numero_do_auto_de_infracao: str
    data_de_vencimento: str
    identificacao_do_agente: str

class User(BaseModel):
    id: int
    name: str
    emai: str


@app.post("/fine-text")
async def post_fine_text(fine_text: Fine_content):
    # do logic, if success

    # leitura do pdf

    # gravação no banco de dados


    return { "msg": "sucess", "code": 200 }

@app.get("/fines/{fine_id}")
async def get_fine(fine_id: int):

    # do logic to communicate with the backend
    fine: Traffic_violation = {
        "nome_do_condutor": "Fulano da Silva Neto",
        "cpf": "123.456.789-00",
        "placa_do_veiculo": "ABC-1234",
        "modelo_do_veiculo": "Sedan",
        "marca_do_veiculo": "Chevrolet",
        "data_e_hora_da_infracao": "01/05/2024 - 14:30",
        "local_da_infracao": "Rua Principal, Bairro Central, Cidade A",
        "tipo_de_infracao": "Excesso de Velocidade",
        "valor_da_multa": "R$ 200,00",
        "ponto_de_referencia": "Próximo ao Posto de Gasolina X",
        "numero_do_auto_de_infracao": "2024001",
        "data_de_vencimento": "15/05/2024",
        "identificacao_do_agente": "Agente Silva - Matrícula: 123456"
    }
    return fine

@app.get("/fines")
async def get_fines():
    # do logic to communicate with the backend
    fine: Traffic_violation = {
        "nome_do_condutor": "Fulano da Silva Neto",
        "cpf": "123.456.789-00",
        "placa_do_veiculo": "ABC-1234",
        "modelo_do_veiculo": "Sedan",
        "marca_do_veiculo": "Chevrolet",
        "data_e_hora_da_infracao": "01/05/2024 - 14:30",
        "local_da_infracao": "Rua Principal, Bairro Central, Cidade A",
        "tipo_de_infracao": "Excesso de Velocidade",
        "valor_da_multa": "R$ 200,00",
        "ponto_de_referencia": "Próximo ao Posto de Gasolina X",
        "numero_do_auto_de_infracao": "2024001",
        "data_de_vencimento": "15/05/2024",
        "identificacao_do_agente": "Agente Silva - Matrícula: 123456"
    }

    fines = [fine, fine, fine, fine]

    return fines

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user: User = { "id": user_id, "name": "Murillo", "email": "email@gmail.com"}

    return user