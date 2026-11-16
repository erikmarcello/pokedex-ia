from pokedex import api
from pokedex.assistente import perguntar

MENU = """
=== Pokédex com IA ===
1. Buscar Pokémon
2. Comparar dois Pokémon
3. Perguntar ao assistente
0. Sair
"""


def comparar(a: str, b: str) -> None:
    p1, p2 = api.buscar_pokemon(a), api.buscar_pokemon(b)
    print(p1.resumo(), "\n")
    print(p2.resumo(), "\n")
    vencedor = p1 if p1.status.total >= p2.status.total else p2
    print(f"Mais forte no total de status: {vencedor.nome}")


def main() -> None:
    while True:
        print(MENU)
        opcao = input("Escolha: ").strip()
        try:
            if opcao == "1":
                print(api.buscar_pokemon(input("Nome ou número: ")).resumo())
            elif opcao == "2":
                comparar(input("Primeiro: "), input("Segundo: "))
            elif opcao == "3":
                print(perguntar(input("Pergunta: ")))
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")
        except api.PokemonNaoEncontrado as e:
            print(f"Pokémon '{e}' não encontrado.")
        except Exception as e:  # rede fora do ar, chave inválida etc.
            print(f"Algo deu errado: {e}")


if __name__ == "__main__":
    main()
