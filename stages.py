from datetime import date

from orders import deadline_status
from storage import save_stages
from utils import format_date, parse_date

STATUSES = ("planned", "in_progress", "done")


def add_stage(
    stages: list[dict],
    order_id: int,
    name: str,
    deadline: date,
) -> dict:
    new_id = max((s["stage_id"] for s in stages), default=0) + 1
    stage = {
        "stage_id": new_id,
        "order_id": order_id,
        "name": name,
        "deadline": format_date(deadline),
        "status": "planned",
    }
    stages.append(stage)
    save_stages(stages)
    return stage


def find_stages_by_order(stages: list[dict], order_id: int) -> list[dict]:
    return [s for s in stages if s["order_id"] == order_id]


def change_stage_status(
    stages: list[dict],
    stage_id: int,
    new_status: str,
) -> bool:
    if new_status not in STATUSES:
        raise ValueError(f"Недопустимый статус: {new_status}")
    for stage in stages:
        if stage["stage_id"] == stage_id:
            stage["status"] = new_status
            save_stages(stages)
            return True
    return False


def sort_stages_by_deadline(stages: list[dict]) -> list[dict]:
    return sorted(stages, key=lambda s: s["deadline"])


def show_stages(
    stages: list[dict],
    order_id: int | None = None,
) -> None:
    if order_id is not None:
        stages = find_stages_by_order(stages, order_id)

    if not stages:
        print("Список этапов пуст.")
        return

    print("\nЭтапы")
    for stage in stages:
        status = deadline_status(parse_date(stage["deadline"]))
        print(
            f"[{stage['stage_id']}] заказ #{stage['order_id']}-"
            f"{stage['name']} | срок {stage['deadline']} | "
            f"{stage['status']} | {status}"
        )
    print()
