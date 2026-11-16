# Pokédex com IA

Pokédex de terminal em Python que consome a [PokeAPI](https://pokeapi.co) e tem um assistente que monta times com vantagem de tipo. Com uma chave gratuita do Gemini, o assistente também responde perguntas livres.

## O que ela faz

- **Buscar** um Pokémon por nome ou número: tipos, altura, peso, habilidades e status.
- **Comparar** dois Pokémon pelo total de status.
- **Assistente:** `monta um time contra pedra` sugere os 6 Pokémon mais fortes da 1ª geração com vantagem sobre o tipo. Com `GEMINI_API_KEY`, aceita qualquer pergunta.
- **Cache local:** cada resposta da API fica salva em `.cache/`, então a segunda busca é instantânea.

## Como rodar

```bash
git clone https://github.com/SEU-USUARIO/pokedex-ia.git
cd pokedex-ia
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
python main.py
```

### Assistente com IA (opcional)

Crie uma chave grátis em https://aistudio.google.com/apikey e defina:

```bash
set GEMINI_API_KEY=sua-chave       # Windows
export GEMINI_API_KEY=sua-chave    # Linux/Mac
```

## Testes

```bash
pytest
```

## Estrutura

```
pokedex/
  modelos.py      classes Pokemon e Status (POO, dataclasses)
  api.py          acesso à PokeAPI com cache
  assistente.py   regras de tipo + integração com o Gemini
main.py           menu no terminal
test_pokedex.py   testes automatizados
```

## O que aprendi

Consumo de API REST, tratamento de erros, orientação a objetos com dataclasses, cache em arquivo, testes com pytest e integração com um modelo de linguagem (LLM).

## Próximos passos

- Salvar os Pokémon em SQLite
- Criar uma API própria com FastAPI
- Interface web com busca e filtro por tipo
