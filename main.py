from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils import gerar_docx
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Questao(BaseModel):
    pergunta: str
    alternativas: List[str]
    respostaCorreta: str

class RequisicaoQuestoes(BaseModel):
    titulo: str
    questoes: List[Questao]

@app.post("/gerar-docx")
def gerar_arquivo(req: RequisicaoQuestoes):
    nome_arquivo = f"{uuid.uuid4()}.docx"
    caminho_arquivo = gerar_docx(req.titulo, req.questoes, nome_arquivo)
    url_download = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{nome_arquivo}"
    return {"downloadUrl": url_download}
