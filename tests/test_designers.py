from designers import add_designer


def test_add_designer() -> None:
    designers: dict = {}
    add_designer(designers, "Виктория", "LOGO")
    assert len(designers) == 1


