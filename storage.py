import json
import os
from typing import Any

from models import Client, Designer, Order, Stage

DATA_DIR = "data"
CLIENTS_FILE = os.path.join(DATA_DIR, "clients.json")
DESIGNERS_FILE = os.path.join(DATA_DIR, "designers.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
STAGES_FILE = os.path.join(DATA_DIR, "stages.json")


def load_json(filename: str, default: Any) -> Any:
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(
            f"Предупреждение: файл {filename} повреждён, "
            f"используются значения по умолчанию."
        )
        return default
    except OSError as error:
        print(f"Ошибка чтения файла {filename}: {error}")
        return default


def save_json(filename: str, data: Any) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка записи файла {filename}: {error}")


def load_clients() -> dict[str, Client]:
    raw = load_json(CLIENTS_FILE, {})
    return {
        client_id: Client.from_data(client_id, data)
        for client_id, data in raw.items()
    }


def save_clients(clients: dict[str, Client]) -> None:
    raw = {
        client_id: client.to_dict()
        for client_id, client in clients.items()
    }
    save_json(CLIENTS_FILE, raw)


def load_designers() -> dict[str, Designer]:
    raw = load_json(DESIGNERS_FILE, {})
    return {
        designer_id: Designer.from_data(designer_id, data)
        for designer_id, data in raw.items()
    }


def save_designers(designers: dict[str, Designer]) -> None:
    raw = {
        designer_id: designer.to_dict()
        for designer_id, designer in designers.items()
    }
    save_json(DESIGNERS_FILE, raw)


def load_orders(
    clients: dict[str, Client],
    designers: dict[str, Designer],
) -> list[Order]:
    raw = load_json(ORDERS_FILE, [])
    orders: list[Order] = []
    for data in raw:
        order = Order.from_data(data, clients, designers)
        if order is not None:
            orders.append(order)
    return orders


def save_orders(orders: list[Order]) -> None:
    raw = [order.to_dict() for order in orders]
    save_json(ORDERS_FILE, raw)


def load_stages(orders: list[Order]) -> list[Stage]:
    raw = load_json(STAGES_FILE, [])
    stages: list[Stage] = []
    for data in raw:
        stage = Stage.from_data(data, orders)
        if stage is not None:
            stages.append(stage)
    return stages


def save_stages(stages: list[Stage]) -> None:
    raw = [stage.to_dict() for stage in stages]
    save_json(STAGES_FILE, raw)