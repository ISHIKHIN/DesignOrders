from clients import add_client, find_client


def test_add_client() -> None:
    clients: dict = {}
    add_client(clients, "ООО Компания", "8 800 555 35 35")
    assert len(clients) == 1


def test_find_client_by_substring() -> None:
    clients: dict = {}
    add_client(clients, "ООО Компания", "8 800 555 35 35")
    found = find_client(clients, "компа")
    assert len(found) == 1


def test_find_client_no_match() -> None:
    clients: dict = {}
    add_client(clients, "ООО Компания", "8 800 555 35 35")
    assert find_client(clients, "что-то") == {}