from datetime import date

from models import Client, Designer, Order
from models.orders import (
    cancel_order,
    create_order,
    filter_orders_by_urgency,
    find_orders_by_client,
    sort_orders_by_deadline,
)


def make_client() -> Client:
    return Client("1", "ООО Компания", "8 800 555 35 35")


def make_designer() -> Designer:
    return Designer("1", "Виктория", "LOGO")


def test_order_creation() -> None:
    client = make_client()
    designer = make_designer()
    order = Order(
        1, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    assert order.id == 1
    assert order.client is client
    assert order.designer is designer
    assert order.design_type == "LOGO"


def test_create_order() -> None:
    orders: list = []
    client = make_client()
    designer = make_designer()
    create_order(
        orders, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    assert len(orders) == 1
    assert isinstance(orders[0], Order)
    assert orders[0].design_type == "LOGO"


def test_cancel_order() -> None:
    orders: list = []
    client = make_client()
    designer = make_designer()
    create_order(
        orders, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    assert cancel_order(orders, 1) is True
    assert orders == []


def test_find_orders_by_client() -> None:
    orders: list = []
    client_1 = make_client()
    client_2 = Client("2", "ИП Иванов", "8 800 000 00 00")
    designer = make_designer()
    create_order(
        orders, client_1, designer, "LOGO", 10000, True,
        date(2026, 12, 31),
    )
    create_order(
        orders, client_2, designer, "BANNER", 5000, False,
        date(2026, 11, 1),
    )
    assert len(find_orders_by_client(orders, client_1)) == 1
    assert len(find_orders_by_client(orders, client_2)) == 1


def test_sort_orders_by_deadline() -> None:
    orders: list = []
    client = make_client()
    designer = make_designer()
    create_order(
        orders, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    create_order(
        orders, client, designer, "BANNER", 5000, False, date(2026, 10, 1)
    )
    sorted_orders = sort_orders_by_deadline(orders)
    assert sorted_orders[0].deadline == date(2026, 10, 1)


def test_filter_orders_by_urgency() -> None:
    orders: list = []
    client = make_client()
    designer = make_designer()
    create_order(
        orders, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    create_order(
        orders, client, designer, "BANNER", 5000, False, date(2026, 10, 1)
    )
    urgent = filter_orders_by_urgency(orders, only_urgent=True)
    assert len(urgent) == 1
    assert urgent[0].design_type == "LOGO"


def test_order_str() -> None:
    client = make_client()
    designer = make_designer()
    order = Order(
        1, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    assert "LOGO" in str(order)
    assert "Срочно" in str(order)


def test_order_to_dict() -> None:
    client = make_client()
    designer = make_designer()
    order = Order(
        1, client, designer, "LOGO", 10000, True, date(2026, 12, 31)
    )
    data = order.to_dict()
    assert data["order_id"] == 1
    assert data["client_id"] == "1"
    assert data["designer_id"] == "1"
    assert data["deadline"] == "2026-12-31"