"""Assistente da Pokédex.

Com GEMINI_API_KEY definida, responde perguntas livres usando o Gemini
(chave gratuita em https://aistudio.google.com/apikey).
Sem chave, usa regras de vantagem de tipo da própria PokeAPI.
"""
import os

import requests

from . import api

TIPOS_PT = {
    "normal": "normal", "fogo": "fire", "agua": "water", "água": "water",
    "planta": "grass", "eletrico": "electric", "elétrico": "electric",
    "gelo": "ice", "lutador": "fighting", "veneno": "poison",
    "terra": "ground", "voador": "flying", "psiquico": "psychic",
    "psíquico": "psychic", "inseto": "bug", "pedra": "rock",
    "fantasma": "ghost", "dragao": "dragon", "dragão": "dragon",
    "sombrio": "dark", "aco": "steel", "aço": "steel", "fada": "fairy",
}


def traduzir_tipo(palavra: str) -> str | None:
    palavra = palavra.lower().strip()
    if palavra in TIPOS_PT:
        return TIPOS_PT[palavra]
    if palavra in TIPOS_PT.values():
        return palavra
    return None


def time_contra(tipo_pt: str, tamanho: int = 6) -> str:
    """Monta um time com os Pokémon mais fortes que têm vantagem sobre o tipo."""
    tipo = traduzir_tipo(tipo_pt)
    if not tipo:
        return f"Não conheço o tipo '{tipo_pt}'."
    fortes = [t["name"] for t in api.relacoes_de_tipo(tipo)["double_damage_from"]]
    candidatos = set()
    for t in fortes:
        candidatos.update(api.pokemons_do_tipo(t))
    pokemons = [api.buscar_pokemon(n) for n in candidatos]
    pokemons.sort(key=lambda p: p.status.total, reverse=True)
    time = pokemons[:tamanho]
    linhas = [f"Tipos fortes contra {tipo_pt}: {', '.join(fortes)}", "Time sugerido (1ª geração):"]
    linhas += [f"  {p.nome} ({'/'.join(p.tipos)}) total {p.status.total}" for p in time]
    return "\n".join(linhas)


def perguntar(pergunta: str) -> str:
    chave = os.getenv("GEMINI_API_KEY")
    if not chave:
        palavras = pergunta.lower().replace("?", "").split()
        if "contra" in palavras:
            i = palavras.index("contra")
            if i + 1 < len(palavras):
                return time_contra(palavras[i + 1])
        return ("Sem GEMINI_API_KEY eu só entendo perguntas como "
                "'monta um time contra pedra'. Configure a chave para perguntas livres.")

    modelo = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    instrucao = ("Você é um especialista em Pokémon. Responda em português, "
                 "de forma curta e prática.\n\nPergunta: " + pergunta)
    resposta = requests.post(
        url, params={"key": chave}, timeout=30,
        json={"contents": [{"parts": [{"text": instrucao}]}]},
    )
    resposta.raise_for_status()
    return resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
