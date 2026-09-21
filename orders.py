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
    return [
        order for order in orders
        if str(order["client_id"]) == client_id
    ]


def sort_orders_by_deadline(orders: list[dict]) -> list[dict]:
    return sorted(orders, key=lambda order: order["deadline"])


def filter_orders_by_urgency(
    orders: list[dict],
    only_urgent: bool = True,
) -> list[dict]:
    return [
        order for order in orders
        if order["is_urgent"] == only_urgent
    ]


def deadline_status(deadline: date, today: date | None = None) -> str:
    if today is None:
        today = date.today()
    diff = (deadline - today).days
    if diff < 0:
        return "Дедлайн просрочен :("
    if diff <= 7:
        return "Дедлайн скоро!"
    return "Дедлайн нескоро :)"


def get_order_status(order: dict) -> str:
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
    if not orders:
        print("Список заказов пуст.")
        return
    print("Заказы")
    for order in orders:
        client = clients.get(str(order["client_id"]), {})
        designer = designers.get(str(order["designer_id"]), {})
        print(get_order_status(order))
        print(f"    Клиент: {client.get('name', '-')}")
        print(f"    Дизайнер: {designer.get('name', '-')}")
    print()
