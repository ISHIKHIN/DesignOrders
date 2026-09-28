from datetime import date

from .clients import Client
from .designers import Designer
from utils import format_date, parse_date


class Order:
    """Заказ на дизайнерские услуги."""

    def __init__(
        self,
        order_id: int,
        client: Client,
        designer: Designer,
        design_type: str,
        price: float,
        is_urgent: bool,
        deadline: date,
    ) -> None:
        self.id = order_id
        self.client = client
        self.designer = designer
        self.design_type = design_type
        self.price = price
        self.is_urgent = is_urgent
        self.deadline = deadline

    @classmethod
    def from_data(
        cls,
        data: dict,
        clients: dict[str, Client],
        designers: dict[str, Designer],
    ) -> "Order | None":
        client = clients.get(str(data["client_id"]))
        designer = designers.get(str(data["designer_id"]))
        if client is None or designer is None:
            return None
        return cls(
            order_id=data["order_id"],
            client=client,
            designer=designer,
            design_type=data["design_type"],
            price=data["price"],
            is_urgent=data["is_urgent"],
            deadline=parse_date(data["deadline"]),
        )

    def to_dict(self) -> dict:
        return {
            "order_id": self.id,
            "client_id": self.client.id,
            "designer_id": self.designer.id,
            "design_type": self.design_type,
            "price": self.price,
            "is_urgent": self.is_urgent,
            "deadline": format_date(self.deadline),
        }

    def get_status(self) -> str:
        urgency = "Срочно" if self.is_urgent else "Не срочно"
        return (
            f"Заказ #{self.id} {self.design_type} "
            f"({urgency}) на сумму {self.price} руб. "
            f"Срок: {format_date(self.deadline)}"
        )

    def deadline_status(self, today: date | None = None) -> str:
        if today is None:
            today = date.today()
        diff = (self.deadline - today).days
        if diff < 0:
            return "Дедлайн просрочен :("
        if diff <= 7:
            return "Дедлайн скоро!"
        return "Дедлайн нескоро :)"

    def __str__(self) -> str:
        return self.get_status()


def create_order(
    orders: list[Order],
    client: Client,
    designer: Designer,
    design_type: str,
    price: float,
    is_urgent: bool,
    deadline: date,
) -> Order:
    new_id = max((order.id for order in orders), default=0) + 1
    order = Order(
        order_id=new_id,
        client=client,
        designer=designer,
        design_type=design_type,
        price=price,
        is_urgent=is_urgent,
        deadline=deadline,
    )
    orders.append(order)
    return order


def cancel_order(orders: list[Order], order_id: int) -> bool:
    for index, order in enumerate(orders):
        if order.id == order_id:
            orders.pop(index)
            return True
    return False


def find_orders_by_client(
    orders: list[Order],
    client: Client,
) -> list[Order]:
    return [order for order in orders if order.client is client]


def sort_orders_by_deadline(orders: list[Order]) -> list[Order]:
    return sorted(orders, key=lambda order: order.deadline)


def filter_orders_by_urgency(
    orders: list[Order],
    only_urgent: bool = True,
) -> list[Order]:
    return [order for order in orders if order.is_urgent == only_urgent]


def show_orders(orders: list[Order]) -> None:
    if not orders:
        print("Список заказов пуст.")
        return
    print("\nЗаказы")
    for order in orders:
        print(order.get_status())
        print(f"    Клиент: {order.client.name}")
        print(f"    Дизайнер: {order.designer.name}")
    print()