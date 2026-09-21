import json
import os
from typing import Any

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
        print(f"Предупреждение: файл {filename} повреждён, "
              f"используются значения по умолчанию.")
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


def load_clients() -> dict[str, dict]:
    return load_json(CLIENTS_FILE, {})


def save_clients(clients: dict[str, dict]) -> None:
    save_json(CLIENTS_FILE, clients)


def load_designers() -> dict[str, dict]:
    return load_json(DESIGNERS_FILE, {})


def save_designers(designers: dict[str, dict]) -> None:
    save_json(DESIGNERS_FILE, designers)


def load_orders() -> list[dict]:
    return load_json(ORDERS_FILE, [])


def save_orders(orders: list[dict]) -> None:
    save_json(ORDERS_FILE, orders)


def load_stages() -> list[dict]:
    return load_json(STAGES_FILE, [])


def save_stages(stages: list[dict]) -> None:
    save_json(STAGES_FILE, stages)
