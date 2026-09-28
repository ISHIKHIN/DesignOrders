from models import Designer
from models.designers import add_designer, find_designer


def test_designer_creation() -> None:
    designer = Designer("1", "Виктория", "LOGO")
    assert designer.id == "1"
    assert designer.name == "Виктория"
    assert designer.specialization == "LOGO"


def test_designer_str() -> None:
    designer = Designer("1", "Виктория", "LOGO")
    assert str(designer) == "[1] Виктория (LOGO)"


def test_add_designer() -> None:
    designers: dict = {}
    add_designer(designers, "Виктория", "LOGO")
    assert len(designers) == 1
    assert isinstance(designers["1"], Designer)


def test_find_designer_by_substring() -> None:
    designers: dict = {}
    add_designer(designers, "Виктория", "LOGO")
    found = find_designer(designers, "викт")
    assert len(found) == 1


def test_designer_to_dict() -> None:
    designer = Designer("1", "Виктория", "LOGO")
    assert designer.to_dict() == {
        "name": "Виктория",
        "specialization": "LOGO",
    }