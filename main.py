from clients import add_client, show_clients
from designers import add_designer, find_designer, show_designers
from orders import (
    cancel_order,
    create_order,
    deadline_status,
    filter_orders_by_urgency,
    find_orders_by_client,
    show_orders,
    sort_orders_by_deadline,
)
from storage import (
    load_clients,
    load_designers,
    load_orders,
)
from utils import input_bool, input_date, input_float, input_int


MENU = """
Система учёта заказов DesignOrders
1. Показать клиентов
2. Добавить клиента
3. Показать дизайнеров
4. Добавить дизайнера
5. Найти дизайнера
6. Показать заказы
7. Добавить заказ
8. Отменить заказ
9. Заказы клиента
10. Сортировать заказы по дедлайну
11. Только срочные заказы
12. Проверить дедлайн
0. Выход
"""


def handle_show_clients(clients: dict) -> None:
    show_clients(clients)


def add_new_client(clients: dict) -> None:
    name = input("Название клиента: ").strip()
    if not name:
        print("Ошибка: название не может быть пустым.")
        return
    phone = input("Телефон: ").strip()
    new_id = add_client(clients, name, phone)
    print(f"Клиент добавлен, идентификатор {new_id}.")


def show_all_designers(designers: dict, orders: list) -> None:
    show_designers(designers, orders)


def add_new_designer(designers: dict) -> None:
    name = input("Имя дизайнера: ").strip()
    if not name:
        print("Ошибка: имя не может быть пустым.")
        return
    specialization = input("Специализация (LOGO/BANNER/...): ").strip()
    new_id = add_designer(designers, name, specialization)
    print(f"Дизайнер добавлен, идентификатор {new_id}.")


def find_exact_designer(designers: dict) -> None:
    query = input("Подстрока для поиска: ").strip()
    found = find_designer(designers, query)
    if not found:
        print("Дизайнеры не найдены.")
        return
    for designer_id, data in found.items():
        print(
            f"[{designer_id}] {data['name']} — {data['specialization']}"
        )


def show_all_orders(
    orders: list,
    clients: dict,
    designers: dict,
) -> None:
    show_orders(orders, clients, designers)


def add_new_order(
    orders: list,
    clients: dict,
    designers: dict,
) -> None:
    if not clients:
        print("Сначала добавьте хотя бы одного клиента.")
        return
    if not designers:
        print("Сначала добавьте хотя бы одного дизайнера.")
        return

    client_id = input("Идентификатор клиента: ").strip()
    if client_id not in clients:
        print("Ошибка: клиент с таким идентификатором не найден.")
        return

    designer_id = input("Идентификатор дизайнера: ").strip()
    if designer_id not in designers:
        print("Ошибка: дизайнер с таким идентификатором не найден.")
        return

    design_type = input("Тип дизайна (LOGO/BANNER/...): ").strip()
    price = input_float("Стоимость, руб.: ")
    is_urgent = input_bool("Срочный заказ? (да/нет): ")
    deadline = input_date("Дедлайн (ДД.ММ.ГГГГ): ")

    order = create_order(
        orders, client_id, designer_id, design_type,
        price, is_urgent, deadline,
    )
    print(f"Заказ #{order['order_id']} создан.")


def handle_cancel_order(orders: list) -> None:
    order_id = input_int("Идентификатор заказа: ")
    if cancel_order(orders, order_id):
        print("Заказ отменён.")
    else:
        print("Заказ с таким идентификатором не найден.")


def handle_orders_by_client(orders: list, clients: dict) -> None:
    client_id = input("Идентификатор клиента: ").strip()
    if client_id not in clients:
        print("Ошибка: клиент не найден.")
        return
    found = find_orders_by_client(orders, client_id)
    if not found:
        print("У клиента нет заказов.")
        return
    for order in found:
        print(
            f"#{order['order_id']} {order['design_type']} — "
            f"{order['price']} руб., срок {order['deadline']}"
        )


def sort_all_orders(orders: list) -> None:
    if not orders:
        print("Список заказов пуст.")
        return
    for order in sort_orders_by_deadline(orders):
        print(f"#{order['order_id']} — срок {order['deadline']}")


def urgent_all_orders(orders: list) -> None:
    urgent = filter_orders_by_urgency(orders, only_urgent=True)
    if not urgent:
        print("Срочных заказов нет.")
        return
    for order in urgent:
        print(
            f"#{order['order_id']} {order['design_type']} — "
            f"срок {order['deadline']}"
        )


def check_deadline() -> None:
    deadline = input_date("Дата дедлайна (ДД.ММ.ГГГГ): ")
    print(deadline_status(deadline))


def main() -> None:
    clients = load_clients()
    designers = load_designers()
    orders = load_orders()

    actions = {
        "1": lambda: handle_show_clients(clients),
        "2": lambda: add_new_client(clients),
        "3": lambda: show_all_designers(designers, orders),
        "4": lambda: add_new_designer(designers),
        "5": lambda: find_exact_designer(designers),
        "6": lambda: show_all_orders(orders, clients, designers),
        "7": lambda: add_new_order(orders, clients, designers),
        "8": lambda: handle_cancel_order(orders),
        "9": lambda: handle_orders_by_client(orders, clients),
        "10": lambda: sort_all_orders(orders),
        "11": lambda: urgent_all_orders(orders),
        "12": lambda: check_deadline(),
    }

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        if choice == "0":
            print("До свидания!")
            break
        action = actions.get(choice)
        if action is None:
            print("Ошибка: неизвестная команда.")
            continue
        try:
            action()
        except (ValueError, KeyError) as error:
            print(f"Ошибка выполнения: {error}")


if __name__ == "__main__":
    main()