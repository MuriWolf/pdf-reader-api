from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class pdf_content(BaseModel):
    content: str

class pdf_full_data(BaseModel):
    id: int
    price: float
    # ...


@app.post("/pdf-text")
async def post_pdf_text(pdf_text: pdf_content):
    # do logic, if success
    return { "msg": "sucess", "code": 200 }

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    # do logic to communicate with the backend
    post: pdf_full_data = {"id": 10, "price": float}
    return post

