from designers import add_designer, get_designer_load


def test_add_designer() -> None:
    designers: dict = {}
    add_designer(designers, "Виктория", "LOGO")
    assert len(designers) == 1


def test_get_designer_load() -> None:
    orders = [
        {"designer_id": "1"},
        {"designer_id": "1"},
        {"designer_id": "2"},
    ]
    assert get_designer_load(orders, "1") == 2
