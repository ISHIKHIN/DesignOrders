from models import Client
from models.clients import add_client, find_client


def test_client_creation() -> None:
    client = Client("1", "ООО Компания", "8 800 555 35 35")
    assert client.id == "1"
    assert client.name == "ООО Компания"
    assert client.phone == "8 800 555 35 35"


def test_client_str() -> None:
    client = Client("1", "ООО Компания", "8 800 555 35 35")
    assert str(client) == "[1] ООО Компания - 8 800 555 35 35"


def test_add_client() -> None:
    clients: dict = {}
    add_client(clients, "ООО Компания", "8 800 555 35 35")
    assert len(clients) == 1
    assert isinstance(clients["1"], Client)


def test_find_client_by_substring() -> None:
    clients: dict = {}
    add_client(clients, "ООО Компания", "8 800 555 35 35")
    found = find_client(clients, "компа")
    assert len(found) == 1


def test_find_client_no_match() -> None:
    clients: dict = {}
    add_client(clients, "ООО Компания", "8 800 555 35 35")
    assert find_client(clients, "что-то") == {}


def test_client_to_dict() -> None:
    client = Client("1", "ООО Компания", "8 800 555 35 35")
    assert client.to_dict() == {
        "name": "ООО Компания",
        "phone": "8 800 555 35 35",
    }