from datetime import date

from orders import (
    cancel_order,
    create_order,
    deadline_status,
    find_orders_by_client,
    sort_orders_by_deadline,
)


def test_create_order() -> None:
    orders: list = []
    create_order(orders, "1", "1", "LOGO", 10000, True, date(2026, 12, 31))
    assert len(orders) == 1
    assert orders[0]["design_type"] == "LOGO"


def test_cancel_order() -> None:
    orders: list = []
    create_order(orders, "1", "1", "LOGO", 10000, True, date(2026, 12, 31))
    assert cancel_order(orders, 1) is True
    assert orders == []


def test_find_orders_by_client() -> None:
    orders: list = []
    create_order(orders, "1", "1", "LOGO", 10000, True, date(2026, 12, 31))
    create_order(orders, "2", "1", "BANNER", 5000, False, date(2026, 11, 1))
    assert len(find_orders_by_client(orders, "1")) == 1


def test_sort_orders_by_deadline() -> None:
    orders: list = []
    create_order(orders, "1", "1", "LOGO", 10000, True, date(2026, 12, 31))
    create_order(orders, "1", "1", "BANNER", 5000, False, date(2026, 10, 1))
    sorted_orders = sort_orders_by_deadline(orders)
    assert sorted_orders[0]["deadline"] == "2026-10-01"


def test_deadline_status_soon() -> None:
    assert deadline_status(
        date(2026, 12, 31), date(2026, 12, 25)
    ) == "Дедлайн скоро!"


def test_deadline_status_overdue() -> None:
    assert deadline_status(
        date(2026, 1, 1), date(2026, 12, 25)
    ) == "Дедлайн просрочен :("
