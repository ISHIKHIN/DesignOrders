from storage import save_designers


def add_designer(
    designers: dict[str, dict],
    name: str,
    specialization: str,
) -> str:
    new_id = str(max((int(key) for key in designers), default=0) + 1)
    designers[new_id] = {"name": name, "specialization": specialization}
    save_designers(designers)
    return new_id

def find_designer(
    designers: dict[str, dict],
    query: str,
) -> dict[str, dict]:
    query_lower = query.lower()
    return {
        designer_id: data
        for designer_id, data in designers.items()
        if query_lower in data["name"].lower()
    }

def show_designers(
    designers: dict[str, dict],
    orders: list[dict],
) -> None:
    if not designers:
        print("Список дизайнеров пуст.")
        return
    print("\n--- Дизайнеры ---")
    for designer_id, data in designers.items():
        print(
            f"[{designer_id}] {data['name']} "
            f"({data['specialization']})"
        )
    print()