from pokedex.modelos import Pokemon
from pokedex.assistente import traduzir_tipo

DADOS = {
    "id": 25, "name": "pikachu", "height": 4, "weight": 60,
    "types": [{"type": {"name": "electric"}}],
    "abilities": [{"ability": {"name": "static"}}],
    "stats": [{"stat": {"name": n}, "base_stat": v} for n, v in [
        ("hp", 35), ("attack", 55), ("defense", 40),
        ("special-attack", 50), ("special-defense", 50), ("speed", 90)]],
}


def test_pokemon_da_api():
    p = Pokemon.da_api(DADOS)
    assert p.nome == "Pikachu"
    assert p.status.total == 320
    assert p.altura_m == 0.4


def test_traduzir_tipo():
    assert traduzir_tipo("Pedra") == "rock"
    assert traduzir_tipo("fire") == "fire"
    assert traduzir_tipo("xyz") is None
