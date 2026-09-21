"""Функции для работы с заказами."""
from datetime import date
from storage import save_orders
from utils import format_date


def create_order(
    orders: list[dict],
    client_id: str,
    designer_id: str,
    design_type: str,
    price: float,
    is_urgent: bool,
    deadline: date,
) -> dict:
    """Создать новый заказ и добавить его в список orders.

    Возвращает созданный заказ.
    """
    new_id = max((order["order_id"] for order in orders), default=0) + 1
    order = {
        "order_id": new_id,
        "client_id": client_id,
        "designer_id": designer_id,
        "design_type": design_type,
        "price": price,
        "is_urgent": is_urgent,
        "deadline": format_date(deadline),
    }
    orders.append(order)
    save_orders(orders)
    return order


def cancel_order(orders: list[dict], order_id: int) -> bool:
    """Удалить заказ по идентификатору.

    Возвращает True, если заказ найден и удалён.
    """
    for index, order in enumerate(orders):
        if order["order_id"] == order_id:
            orders.pop(index)
            save_orders(orders)
            return True
    return False


def find_orders_by_client(
    orders: list[dict],
    client_id: str,
) -> list[dict]:
    """Найти заказы клиента по его идентификатору."""
    return [
        order for order in orders
        if str(order["client_id"]) == client_id
    ]


def sort_orders_by_deadline(orders: list[dict]) -> list[dict]:
    """Отсортировать заказы по дате дедлайна (по возрастанию)."""
    return sorted(orders, key=lambda order: order["deadline"])


def filter_orders_by_urgency(
    orders: list[dict],
    only_urgent: bool = True,
) -> list[dict]:
    """Отфильтровать заказы по признаку срочности."""
    return [
        order for order in orders
        if order["is_urgent"] == only_urgent
    ]


def deadline_status(deadline: date, today: date | None = None) -> str:
    """Вернуть текстовый статус дедлайна.

    Функция переработана из ПР1: today вынесен в параметр,
    чтобы её можно было тестировать без привязки к текущей дате.
    """
    if today is None:
        today = date.today()
    diff = (deadline - today).days
    if diff < 0:
        return "Дедлайн просрочен :("
    if diff <= 7:
        return "Дедлайн скоро!"
    return "Дедлайн нескоро :)"


def get_order_status(order: dict) -> str:
    """Вернуть текстовое описание заказа.

    Заменяет функцию create_order() из ПР1, которая возвращала
    готовую строку — теперь формирование описания вынесено сюда.
    """
    urgency = "Срочно" if order["is_urgent"] else "Не срочно"
    return (
        f"Заказ #{order['order_id']} {order['design_type']} "
        f"({urgency}) на сумму {order['price']} руб. "
        f"Срок: {order['deadline']}"
    )


def show_orders(
    orders: list[dict],
    clients: dict[str, dict],
    designers: dict[str, dict],
) -> None:
    """Вывести список заказов с расшифровкой клиента и дизайнера."""
    if not orders:
        print("Список заказов пуст.")
        return
    print("\n--- Заказы ---")
    for order in orders:
        client = clients.get(str(order["client_id"]), {})
        designer = designers.get(str(order["designer_id"]), {})
        print(get_order_status(order))
        print(f"    Клиент: {client.get('name', '—')}")
        print(f"    Дизайнер: {designer.get('name', '—')}")
    print()