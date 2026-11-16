# Pokédex com IA

Pokédex em Python, com versão web (FastAPI) e de terminal, que consome a [PokeAPI](https://pokeapi.co) e tem um assistente que monta times com vantagem de tipo. Com uma chave gratuita do Gemini, o assistente também responde perguntas livres.

## O que ela faz

- **Buscar** um Pokémon por nome ou número: tipos, altura, peso, habilidades e status.
- **Comparar** dois Pokémon pelo total de status.
- **Assistente:** `monta um time contra pedra` sugere os 6 Pokémon mais fortes da 1ª geração com vantagem sobre o tipo. Com `GEMINI_API_KEY`, aceita qualquer pergunta.
- **Cache local:** cada resposta da API fica salva em `.cache/`, então a segunda busca é instantânea.

## Versão web

```bash
pip install -r requirements.txt
uvicorn web:app --reload
```

Abra http://localhost:8000. A documentação interativa da API fica em http://localhost:8000/docs.

| Rota | O que faz |
|---|---|
| `GET /api/pokemon/{nome}` | Dados, status e imagem de um Pokémon |
| `GET /api/comparar?a=x&b=y` | Compara dois Pokémon |
| `POST /api/assistente` | Pergunta ao assistente (`{"pergunta": "..."}`) |

## Como rodar (terminal)

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
web.py            API REST (FastAPI) + página
static/index.html interface web (busca, comparação, assistente)
main.py           menu no terminal
test_pokedex.py   testes automatizados
```

## O que aprendi

Criação e consumo de API REST (FastAPI), tratamento de erros, orientação a objetos com dataclasses, cache em arquivo, testes com pytest e integração com um modelo de linguagem (LLM).

## Próximos passos

- Salvar os Pokémon em SQLite
- Publicar online (Render)
- Filtro por tipo na interface
