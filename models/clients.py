class Client:

    def __init__(self, client_id: str, name: str, phone: str) -> None:
        self.id = client_id
        self.name = name
        self.phone = phone

    @classmethod
    def from_data(cls, client_id: str, data: dict) -> "Client":
        return cls(
            client_id=client_id,
            name=data["name"],
            phone=data["phone"],
        )

    def to_dict(self) -> dict:
        return {"name": self.name, "phone": self.phone}

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} - {self.phone}"


def add_client(
    clients: dict[str, Client],
    name: str,
    phone: str,
) -> Client:
    new_id = str(max((int(key) for key in clients), default=0) + 1)
    client = Client(new_id, name, phone)
    clients[new_id] = client
    return client


def find_client(
    clients: dict[str, Client],
    query: str,
) -> dict[str, Client]:
    query_lower = query.lower()
    return {
        client_id: client
        for client_id, client in clients.items()
        if query_lower in client.name.lower()
    }


def show_clients(clients: dict[str, Client]) -> None:
    if not clients:
        print("Список клиентов пуст.")
        return
    print("\nКлиенты")
    for client in clients.values():
        print(client)
    print()