from datetime import date

from .orders import Order
from utils import format_date, parse_date

STATUSES = ("planned", "in_progress", "done")


class Stage:
    """Этап выполнения заказа."""

    def __init__(
        self,
        stage_id: int,
        order: Order,
        name: str,
        deadline: date,
        status: str = "planned",
    ) -> None:
        self.id = stage_id
        self.order = order
        self.name = name
        self.deadline = deadline
        self.status = status

    @classmethod
    def from_data(
        cls,
        data: dict,
        orders: list[Order],
    ) -> "Stage | None":
        order = next(
            (o for o in orders if o.id == data["order_id"]),
            None,
        )
        if order is None:
            return None
        return cls(
            stage_id=data["stage_id"],
            order=order,
            name=data["name"],
            deadline=parse_date(data["deadline"]),
            status=data["status"],
        )

    def to_dict(self) -> dict:
        return {
            "stage_id": self.id,
            "order_id": self.order.id,
            "name": self.name,
            "deadline": format_date(self.deadline),
            "status": self.status,
        }

    def change_status(self, new_status: str) -> None:
        if new_status not in STATUSES:
            raise ValueError(f"Недопустимый статус: {new_status}")
        self.status = new_status

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
        return (
            f"[{self.id}] заказ #{self.order.id} — {self.name} | "
            f"срок {format_date(self.deadline)} | {self.status} | "
            f"{self.deadline_status()}"
        )


def add_stage(
    stages: list[Stage],
    order: Order,
    name: str,
    deadline: date,
) -> Stage:
    new_id = max((stage.id for stage in stages), default=0) + 1
    stage = Stage(
        stage_id=new_id,
        order=order,
        name=name,
        deadline=deadline,
    )
    stages.append(stage)
    return stage


def find_stages_by_order(
    stages: list[Stage],
    order: Order,
) -> list[Stage]:
    return [stage for stage in stages if stage.order is order]


def change_stage_status(
    stages: list[Stage],
    stage_id: int,
    new_status: str,
) -> bool:
    if new_status not in STATUSES:
        raise ValueError(f"Недопустимый статус: {new_status}")
    for stage in stages:
        if stage.id == stage_id:
            stage.change_status(new_status)
            return True
    return False


def sort_stages_by_deadline(stages: list[Stage]) -> list[Stage]:
    return sorted(stages, key=lambda stage: stage.deadline)


def show_stages(
    stages: list[Stage],
    order: Order | None = None,
) -> None:
    if order is not None:
        stages = find_stages_by_order(stages, order)

    if not stages:
        print("Список этапов пуст.")
        return

    print("\nЭтапы")
    for stage in stages:
        print(stage)
    print()