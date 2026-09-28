from datetime import date

from models import Client, Designer, Order, Stage
from models.orders import create_order
from models.stages import (
    STATUSES,
    add_stage,
    change_stage_status,
    find_stages_by_order,
    sort_stages_by_deadline,
)


def make_order() -> Order:
    client = Client("1", "ООО Компания", "8 800 555 35 35")
    designer = Designer("1", "Виктория", "LOGO")
    return Order(
        1, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )


def test_stage_creation() -> None:
    order = make_order()
    stage = Stage(1, order, "Концепт-арт", date(2026, 10, 15))
    assert stage.id == 1
    assert stage.order is order
    assert stage.name == "Концепт-арт"
    assert stage.deadline == date(2026, 10, 15)
    assert stage.status == "planned"


def test_stage_str() -> None:
    order = make_order()
    stage = Stage(1, order, "Концепт-арт", date(2026, 10, 15))
    text = str(stage)
    assert "Концепт-арт" in text
    assert "planned" in text
    assert "заказ #1" in text


def test_add_stage() -> None:
    orders: list = []
    client = Client("1", "ООО Компания", "8 800 555 35 35")
    designer = Designer("1", "Виктория", "LOGO")
    order = create_order(
        orders, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    stages: list = []
    stage = add_stage(stages, order, "Концепт-арт", date(2026, 10, 15))
    assert len(stages) == 1
    assert isinstance(stage, Stage)
    assert stage.order is order


def test_find_stages_by_order() -> None:
    orders: list = []
    client = Client("1", "ООО Компания", "8 800 555 35 35")
    designer = Designer("1", "Виктория", "LOGO")
    order_1 = create_order(
        orders, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    order_2 = create_order(
        orders, client, designer, "BANNER", 5000, False, date(2026, 11, 1)
    )
    stages: list = []
    add_stage(stages, order_1, "Концепт-арт", date(2026, 10, 15))
    add_stage(stages, order_1, "Концепция", date(2026, 11, 20))
    add_stage(stages, order_2, "Макет", date(2026, 11, 1))

    found_1 = find_stages_by_order(stages, order_1)
    found_2 = find_stages_by_order(stages, order_2)
    assert len(found_1) == 2
    assert len(found_2) == 1


def test_change_stage_status() -> None:
    order = make_order()
    stages: list = []
    stage = add_stage(stages, order, "Концепт-арт", date(2026, 10, 15))
    result = change_stage_status(stages, stage.id, "in_progress")
    assert result is True
    assert stage.status == "in_progress"


def test_change_stage_status_invalid() -> None:
    order = make_order()
    stages: list = []
    stage = add_stage(stages, order, "Концепт-арт", date(2026, 10, 15))
    try:
        change_stage_status(stages, stage.id, "unknown")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        assert True


def test_change_stage_status_not_found() -> None:
    order = make_order()
    stages: list = []
    add_stage(stages, order, "Концепт-арт", date(2026, 10, 15))
    assert change_stage_status(stages, 999, "done") is False


def test_change_status_method() -> None:
    order = make_order()
    stage = Stage(1, order, "Концепт-арт", date(2026, 10, 15))
    stage.change_status("done")
    assert stage.status == "done"


def test_change_status_method_invalid() -> None:
    order = make_order()
    stage = Stage(1, order, "Концепт-арт", date(2026, 10, 15))
    try:
        stage.change_status("unknown")
        assert False, "Ожидалось исключение ValueError"
    except ValueError:
        assert True


def test_sort_stages_by_deadline() -> None:
    order = make_order()
    stages: list = []
    add_stage(stages, order, "Макет", date(2026, 11, 1))
    add_stage(stages, order, "Концепт-арт", date(2026, 10, 15))
    add_stage(stages, order, "Концепция", date(2026, 11, 20))
    sorted_stages = sort_stages_by_deadline(stages)
    assert sorted_stages[0].name == "Концепт-арт"
    assert sorted_stages[1].name == "Макет"
    assert sorted_stages[2].name == "Концепция"


def test_stage_to_dict() -> None:
    order = make_order()
    stage = Stage(1, order, "Концепт-арт", date(2026, 10, 15))
    data = stage.to_dict()
    assert data["stage_id"] == 1
    assert data["order_id"] == 1
    assert data["name"] == "Концепт-арт"
    assert data["deadline"] == "2026-10-15"
    assert data["status"] == "planned"


def test_stage_from_data() -> None:
    order = make_order()
    orders = [order]
    data = {
        "stage_id": 5,
        "order_id": 1,
        "name": "Концепт-арт",
        "deadline": "2026-10-15",
        "status": "done",
    }
    stage = Stage.from_data(data, orders)
    assert stage is not None
    assert stage.id == 5
    assert stage.order is order
    assert stage.name == "Концепт-арт"
    assert stage.deadline == date(2026, 10, 15)
    assert stage.status == "done"


def test_stage_from_data_order_not_found() -> None:
    data = {
        "stage_id": 5,
        "order_id": 999,
        "name": "Концепт-арт",
        "deadline": "2026-10-15",
        "status": "planned",
    }
    assert Stage.from_data(data, []) is None


def test_statuses_constant() -> None:
    assert STATUSES == ("planned", "in_progress", "done")