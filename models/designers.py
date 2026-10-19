class Designer:

    def __init__(
        self,
        designer_id: str,
        name: str,
        specialization: str,
    ) -> None:
        self.id = designer_id
        self.name = name
        self.specialization = specialization

    @classmethod
    def from_data(cls, designer_id: str, data: dict) -> "Designer":
        return cls(
            designer_id=designer_id,
            name=data["name"],
            specialization=data["specialization"],
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "specialization": self.specialization,
        }

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.specialization})"


def add_designer(
    designers: dict[str, Designer],
    name: str,
    specialization: str,
) -> Designer:
    new_id = str(max((int(key) for key in designers), default=0) + 1)
    designer = Designer(new_id, name, specialization)
    designers[new_id] = designer
    return designer


def find_designer(
    designers: dict[str, Designer],
    query: str,
) -> dict[str, Designer]:
    query_lower = query.lower()
    return {
        designer_id: designer
        for designer_id, designer in designers.items()
        if query_lower in designer.name.lower()
    }


def show_designers(designers: dict[str, Designer]) -> None:
    if not designers:
        print("Список дизайнеров пуст.")
        return
    print("\nДизайнеры")
    for designer in designers.values():
        print(designer)
    print()