"""Acesso à PokeAPI com cache local em JSON (menos requisições, mais rápido)."""
import json
from pathlib import Path

import requests

from .modelos import Pokemon

URL_BASE = "https://pokeapi.co/api/v2"
CACHE = Path(__file__).resolve().parent.parent / ".cache"


class PokemonNaoEncontrado(Exception):
    pass


def _get(caminho: str) -> dict:
    CACHE.mkdir(exist_ok=True)
    arquivo = CACHE / (caminho.replace("/", "_") + ".json")
    if arquivo.exists():
        return json.loads(arquivo.read_text(encoding="utf-8"))
    resposta = requests.get(f"{URL_BASE}/{caminho}", timeout=15)
    if resposta.status_code == 404:
        raise PokemonNaoEncontrado(caminho.split("/")[-1])
    resposta.raise_for_status()
    dados = resposta.json()
    arquivo.write_text(json.dumps(dados), encoding="utf-8")
    return dados


def buscar_pokemon(nome_ou_numero: str) -> Pokemon:
    chave = str(nome_ou_numero).lower().strip()
    return Pokemon.da_api(_get(f"pokemon/{chave}"))


def relacoes_de_tipo(tipo: str) -> dict:
    """Retorna as relações de dano de um tipo (ex.: 'rock')."""
    return _get(f"type/{tipo.lower().strip()}")["damage_relations"]


def pokemons_do_tipo(tipo: str, ate_numero: int = 151) -> list[str]:
    """Pokémon de um tipo, filtrados até um número da Pokédex (padrão: 1ª geração)."""
    dados = _get(f"type/{tipo.lower().strip()}")
    nomes = []
    for item in dados["pokemon"]:
        numero = int(item["pokemon"]["url"].rstrip("/").split("/")[-1])
        if numero <= ate_numero:
            nomes.append(item["pokemon"]["name"])
    return nomes
