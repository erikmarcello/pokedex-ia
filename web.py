"""API REST da Pokédex com FastAPI + página web.

Rodar:  uvicorn web:app --reload   e abrir http://localhost:8000
"""
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from pokedex import api
from pokedex.assistente import perguntar

app = FastAPI(title="Pokédex com IA", version="2.0")
PAGINA = Path(__file__).parent / "static" / "index.html"


def _pokemon_dict(nome: str) -> dict:
    try:
        p = api.buscar_pokemon(nome)
    except api.PokemonNaoEncontrado:
        raise HTTPException(404, f"Pokémon '{nome}' não encontrado")
    dados = asdict(p)
    dados["status"]["total"] = p.status.total
    return dados


@app.get("/", include_in_schema=False)
def pagina():
    return FileResponse(PAGINA)


@app.get("/api/pokemon/{nome}")
def pokemon(nome: str):
    return _pokemon_dict(nome)


@app.get("/api/comparar")
def comparar(a: str, b: str):
    p1, p2 = _pokemon_dict(a), _pokemon_dict(b)
    vencedor = p1 if p1["status"]["total"] >= p2["status"]["total"] else p2
    return {"a": p1, "b": p2, "vencedor": vencedor["nome"]}


class Pergunta(BaseModel):
    pergunta: str


@app.post("/api/assistente")
def assistente(body: Pergunta):
    try:
        return {"resposta": perguntar(body.pergunta)}
    except Exception as e:
        raise HTTPException(502, f"Assistente indisponível: {e}")
