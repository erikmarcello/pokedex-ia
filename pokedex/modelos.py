from dataclasses import dataclass, field


@dataclass
class Status:
    hp: int
    ataque: int
    defesa: int
    ataque_especial: int
    defesa_especial: int
    velocidade: int

    @property
    def total(self) -> int:
        return (self.hp + self.ataque + self.defesa + self.ataque_especial
                + self.defesa_especial + self.velocidade)


def _imagem(sprites: dict) -> str:
    arte = sprites.get("other", {}).get("official-artwork", {}).get("front_default")
    return arte or sprites.get("front_default") or ""


@dataclass
class Pokemon:
    numero: int
    nome: str
    tipos: list[str]
    altura_m: float
    peso_kg: float
    status: Status
    habilidades: list[str] = field(default_factory=list)
    imagem: str = ""

    @classmethod
    def da_api(cls, dados: dict) -> "Pokemon":
        s = {item["stat"]["name"]: item["base_stat"] for item in dados["stats"]}
        return cls(
            numero=dados["id"],
            nome=dados["name"].capitalize(),
            tipos=[t["type"]["name"] for t in dados["types"]],
            altura_m=dados["height"] / 10,
            peso_kg=dados["weight"] / 10,
            status=Status(
                hp=s["hp"], ataque=s["attack"], defesa=s["defense"],
                ataque_especial=s["special-attack"],
                defesa_especial=s["special-defense"], velocidade=s["speed"],
            ),
            habilidades=[h["ability"]["name"] for h in dados["abilities"]],
            imagem=_imagem(dados.get("sprites", {})),
        )

    def resumo(self) -> str:
        st = self.status
        return (
            f"#{self.numero} {self.nome}\n"
            f"Tipos: {', '.join(self.tipos)}\n"
            f"Altura: {self.altura_m} m | Peso: {self.peso_kg} kg\n"
            f"Habilidades: {', '.join(self.habilidades)}\n"
            f"HP {st.hp} | Atq {st.ataque} | Def {st.defesa} | "
            f"AtqEsp {st.ataque_especial} | DefEsp {st.defesa_especial} | "
            f"Vel {st.velocidade} | Total {st.total}"
        )
