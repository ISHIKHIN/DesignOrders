from datetime import date

from models import Client, Designer, Order, Stage
from models.clients import add_client, show_clients
from models.designers import (
    add_designer,
    find_designer,
    show_designers,
)
from models.orders import (
    cancel_order,
    create_order,
    filter_orders_by_urgency,
    find_order_by_id,
    find_orders_by_client,
    show_orders,
    sort_orders_by_deadline,
)
from models.stages import (
    STATUSES,
    add_stage,
    change_stage_status,
    find_stage_by_id,
    find_stages_by_order,
    remove_stages_by_order,
    show_stages,
    sort_stages_by_deadline,
    update_stage,
)
from storage import (
    load_clients,
    load_designers,
    load_orders,
    load_stages,
    save_clients,
    save_designers,
    save_orders,
    save_stages,
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
13. Показать этапы
14. Добавить этап
15. Сменить статус этапа
16. Сортировать этапы по дедлайну
17. Редактировать этап
0. Выход
"""


def handle_show_clients(clients: dict[str, Client]) -> None:
    show_clients(clients)


def add_new_client(clients: dict[str, Client]) -> None:
    name = input("Название клиента: ").strip()
    if not name:
        print("Ошибка: название не может быть пустым.")
        return
    phone = input("Телефон: ").strip()
    client = add_client(clients, name, phone)
    save_clients(clients)
    print(f"Клиент добавлен, идентификатор {client.id}.")


def show_all_designers(designers: dict[str, Designer]) -> None:
    show_designers(designers)


def add_new_designer(designers: dict[str, Designer]) -> None:
    name = input("Имя дизайнера: ").strip()
    if not name:
        print("Ошибка: имя не может быть пустым.")
        return
    specialization = input("Специализация (LOGO/BANNER/...): ").strip()
    designer = add_designer(designers, name, specialization)
    save_designers(designers)
    print(f"Дизайнер добавлен, идентификатор {designer.id}.")


def find_exact_designer(designers: dict[str, Designer]) -> None:
    query = input("Подстрока для поиска: ").strip()
    found = find_designer(designers, query)
    if not found:
        print("Дизайнеры не найдены.")
        return
    for designer in found.values():
        print(designer)


def show_all_orders(orders: list[Order]) -> None:
    show_orders(orders)


def add_new_order(
    orders: list[Order],
    clients: dict[str, Client],
    designers: dict[str, Designer],
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
    client = clients[client_id]

    designer_id = input("Идентификатор дизайнера: ").strip()
    if designer_id not in designers:
        print("Ошибка: дизайнер с таким идентификатором не найден.")
        return
    designer = designers[designer_id]

    design_type = input("Тип дизайна (LOGO/BANNER/...): ").strip()
    price = input_float("Стоимость, руб.: ")
    is_urgent = input_bool("Срочный заказ? (да/нет): ")
    deadline = input_date("Дедлайн (ДД.ММ.ГГГГ): ")

    order = create_order(
        orders,
        client,
        designer,
        design_type,
        price,
        is_urgent,
        deadline,
    )
    save_orders(orders)
    print(f"Заказ #{order.id} создан.")


def handle_cancel_order(
    orders: list[Order],
    stages: list[Stage],
) -> None:
    order_id = input_int("Идентификатор заказа: ")
    removed_order = cancel_order(orders, order_id)
    if removed_order is None:
        print("Заказ с таким идентификатором не найден.")
        return
    removed_stages = remove_stages_by_order(stages, order_id)
    save_orders(orders)
    save_stages(stages)
    print(
        f"Заказ #{order_id} отменён. "
        f"Удалено этапов: {removed_stages}."
    )


def handle_orders_by_client(
    orders: list[Order],
    clients: dict[str, Client],
) -> None:
    client_id = input("Идентификатор клиента: ").strip()
    if client_id not in clients:
        print("Ошибка: клиент не найден.")
        return
    client = clients[client_id]
    found = find_orders_by_client(orders, client)
    if not found:
        print("У клиента нет заказов.")
        return
    for order in found:
        print(
            f"#{order.id} {order.design_type} - "
            f"{order.price} руб., срок {order.deadline}"
        )


def sort_all_orders(orders: list[Order]) -> None:
    if not orders:
        print("Список заказов пуст.")
        return
    for order in sort_orders_by_deadline(orders):
        print(f"#{order.id} - срок {order.deadline}")


def urgent_all_orders(orders: list[Order]) -> None:
    urgent = filter_orders_by_urgency(orders, only_urgent=True)
    if not urgent:
        print("Срочных заказов нет.")
        return
    for order in urgent:
        print(
            f"#{order.id} {order.design_type} - "
            f"срок {order.deadline}"
        )


def check_deadline() -> None:
    deadline = input_date("Дата дедлайна (ДД.ММ.ГГГГ): ")
    diff = (deadline - date.today()).days
    if diff < 0:
        print("Дедлайн просрочен :(")
    elif diff <= 7:
        print("Дедлайн скоро!")
    else:
        print("Дедлайн нескоро :)")


def handle_show_stages(
    stages: list[Stage],
    orders: list[Order],
) -> None:
    if not orders:
        print("Список заказов пуст.")
        return
    order_id = input_int("ID заказа: ")
    order = find_order_by_id(orders, order_id)
    if order is None:
        print("Заказ с таким идентификатором не найден.")
        return
    show_stages(stages, order)


def handle_add_stage(
    stages: list[Stage],
    orders: list[Order],
) -> None:
    if not orders:
        print("Сначала добавьте хотя бы один заказ.")
        return
    order_id = input_int("ID заказа: ")
    order = find_order_by_id(orders, order_id)
    if order is None:
        print("Заказ с таким идентификатором не найден.")
        return
    name = input("Название этапа: ").strip()
    if not name:
        print("Ошибка: название не может быть пустым.")
        return
    deadline = input_date("Дедлайн этапа (ДД.ММ.ГГГГ): ")
    stage = add_stage(stages, order, name, deadline)
    save_stages(stages)
    print(f"Этап #{stage.id} добавлен.")


def handle_change_stage_status(stages: list[Stage]) -> None:
    stage_id = input_int("ID этапа: ")
    new_status = input(
        f"Новый статус ({'/'.join(STATUSES)}): "
    ).strip()
    try:
        if change_stage_status(stages, stage_id, new_status):
            save_stages(stages)
            print("Статус изменён.")
        else:
            print("Этап с таким идентификатором не найден.")
    except ValueError as error:
        print(f"Ошибка: {error}")


def handle_sort_stages(stages: list[Stage]) -> None:
    if not stages:
        print("Список этапов пуст.")
        return
    for stage in sort_stages_by_deadline(stages):
        print(stage)


def _ask_optional(prompt: str, current: str) -> str | None:
    """Спросить значение. Enter — оставить текущее."""
    raw = input(f"{prompt} [{current}]: ").strip()
    if not raw:
        return None
    return raw


def handle_edit_stage(
    stages: list[Stage],
    orders: list[Order],
) -> None:
    if not stages:
        print("Список этапов пуст.")
        return

    stage_id = input_int("ID этапа для редактирования: ")
    stage = find_stage_by_id(stages, stage_id)
    if stage is None:
        print("Этап с таким идентификатором не найден.")
        return

    print(f"Текущий этап: {stage}")
    print("Enter — оставить поле без изменений.")

    new_name = _ask_optional("Новое название", stage.name)

    new_deadline: date | None = None
    raw_deadline = input(
        f"Новый дедлайн (ДД.ММ.ГГГГ) "
        f"[{stage.deadline.strftime('%d.%m.%Y')}]: "
    ).strip()
    if raw_deadline:
        from utils import parse_date_user
        try:
            new_deadline = parse_date_user(raw_deadline)
        except ValueError:
            print("Ошибка: неверный формат даты. Изменение отменено.")
            return

    new_status = _ask_optional(
        f"Новый статус ({'/'.join(STATUSES)})",
        stage.status,
    )

    new_order: Order | None = None
    raw_order = input(
        f"ID нового заказа [{stage.order.id}] (Enter — оставить): "
    ).strip()
    if raw_order:
        try:
            order_id = int(raw_order)
        except ValueError:
            print("Ошибка: ID заказа должен быть числом.")
            return
        candidate = find_order_by_id(orders, order_id)
        if candidate is None:
            print("Заказ с таким идентификатором не найден.")
            return
        new_order = candidate

    try:
        update_stage(
            stage,
            name=new_name,
            deadline=new_deadline,
            status=new_status,
            order=new_order,
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_stages(stages)
    print(f"Этап обновлён: {stage}")


def main() -> None:
    clients = load_clients()
    designers = load_designers()
    orders = load_orders(clients, designers)
    stages = load_stages(orders)

    actions = {
        "1": lambda: handle_show_clients(clients),
        "2": lambda: add_new_client(clients),
        "3": lambda: show_all_designers(designers),
        "4": lambda: add_new_designer(designers),
        "5": lambda: find_exact_designer(designers),
        "6": lambda: show_all_orders(orders),
        "7": lambda: add_new_order(orders, clients, designers),
        "8": lambda: handle_cancel_order(orders, stages),
        "9": lambda: handle_orders_by_client(orders, clients),
        "10": lambda: sort_all_orders(orders),
        "11": lambda: urgent_all_orders(orders),
        "12": lambda: check_deadline(),
        "13": lambda: handle_show_stages(stages, orders),
        "14": lambda: handle_add_stage(stages, orders),
        "15": lambda: handle_change_stage_status(stages),
        "16": lambda: handle_sort_stages(stages),
        "17": lambda: handle_edit_stage(stages, orders),
    }

    while True:
        print(MENU)
        try:
            choice = input("Выберите действие: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nДо свидания!")
            break
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