from storage import save_clients


def add_client(clients: dict[str, dict], name: str, phone: str) -> str:
    new_id = str(len(clients) + 1)
    clients[new_id] = {"name": name, "phone": phone}
    save_clients(clients)
    return new_id


def find_client(clients: dict[str, dict], query: str) -> dict[str, dict]:
    found = {}
    for cid, data in clients.items():
        if query.lower() in data["name"].lower():
            found[cid] = data
    return found


def show_clients(clients: dict[str, dict]) -> None:
    if not clients:
        print("Список клиентов пуст.")
        return
    print("\nКлиенты")
    for cid, data in clients.items():
        print(f"[{cid}] {data['name']} - {data['phone']}")
