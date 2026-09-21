from datetime import date, datetime


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")


def input_date(prompt: str) -> date:
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: неверный формат даты. Пример: 31.12.2026")


def input_bool(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False
        print("Ошибка: ответьте 'да' или 'нет'.")


def format_date(value: date) -> str:
    return value.strftime("%Y-%m-%d")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()