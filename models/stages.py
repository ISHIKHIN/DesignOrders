from datetime import date

from .orders import Order
from utils import format_date, parse_date

STATUSES = ("planned", "in_progress", "done")

# Глобальный счётчик, чтобы id этапов не переиспользовались.
_next_stage_id = [0]


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


def next_stage_id(stages: list[Stage]) -> int:
    """Выдать следующий id этапа без переиспользования."""
    max_active = max((stage.id for stage in stages), default=0)
    return max(max_active, _next_stage_id[0]) + 1


def remember_stage_id(stage_id: int) -> None:
    """Запомнить использованный id этапа."""
    if stage_id > _next_stage_id[0]:
        _next_stage_id[0] = stage_id


def add_stage(
    stages: list[Stage],
    order: Order,
    name: str,
    deadline: date,
) -> Stage:
    new_id = next_stage_id(stages)
    remember_stage_id(new_id)
    stage = Stage(
        stage_id=new_id,
        order=order,
        name=name,
        deadline=deadline,
    )
    stages.append(stage)
    return stage


def find_stage_by_id(
    stages: list[Stage],
    stage_id: int,
) -> Stage | None:
    """Найти этап по id или вернуть None."""
    return next((stage for stage in stages if stage.id == stage_id), None)


def find_stages_by_order(
    stages: list[Stage],
    order: Order,
) -> list[Stage]:
    return [stage for stage in stages if stage.order.id == order.id]


def remove_stages_by_order(
    stages: list[Stage],
    order_id: int,
) -> int:
    """Удалить все этапы указанного заказа.

    Возвращает количество удалённых этапов.
    """
    before = len(stages)
    stages[:] = [stage for stage in stages if stage.order.id != order_id]
    return before - len(stages)


def update_stage(
    stage: Stage,
    *,
    name: str | None = None,
    deadline: date | None = None,
    status: str | None = None,
    order: Order | None = None,
) -> Stage:
    """Обновить поля этапа.

    Передавайте только те параметры, которые нужно изменить.
    Если параметр равен None — поле остаётся прежним.
    """
    if name is not None:
        if not name.strip():
            raise ValueError("Название этапа не может быть пустым.")
        stage.name = name.strip()
    if deadline is not None:
        stage.deadline = deadline
    if status is not None:
        stage.change_status(status)
    if order is not None:
        stage.order = order
    return stage


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