# DesignOrders — система учёта заказов на дизайн

## Назначение

Приложение для приёма, оценки и распределения заказов на дизайнерские
услуги. Позволяет менеджеру создать заказ, рассчитать стоимость
с учётом срочности, назначить дизайнера и отслеживать сроки выполнения.

Консольная версия приложения (ПР3) дополнена веб-интерфейсом на Django (ПР5).

## Целевая аудитория

- дизайн-студии и агентства;
- фрилансеры-дизайнеры;
- менеджеры, работающие с клиентскими заказами;
- крупные компании или физические лица со своим бизнесом.

## Предметная область

Приём и учёт заказов на дизайн, отслеживание этапов выполнения,
назначение дизайнеров, контроль дедлайнов.

Основные объекты:

- `Client` — клиент;
- `Designer` — дизайнер;
- `Order` — заказ;
- `Stage` — этап выполнения заказа.

## Используемые технологии

- Python 3.11;
- Django 5.2 — веб-фреймворк;
- HTML, CSS, Bootstrap 5.3 (CDN) — оформление страниц;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода.

## Основные классы

### Client

Атрибуты: `id`, `name`, `phone`.
Методы: `from_data()`, `to_dict()`, `__str__()`.
Функции модуля: `add_client()`, `find_client()`, `show_clients()`.

### Designer

Атрибуты: `id`, `name`, `specialization`.
Методы: `from_data()`, `to_dict()`, `__str__()`.
Функции модуля: `add_designer()`, `find_designer()`, `show_designers()`.

### Order

Атрибуты: `id`, `client`, `designer`, `design_type`, `price`,
`is_urgent`, `deadline`.
Методы: `from_data()`, `to_dict()`, `get_status()`,
`deadline_status()`, `__str__()`.
Функции модуля: `next_order_id()`, `remember_order_id()`,
`create_order()`, `find_order_by_id()`, `cancel_order()`,
`find_orders_by_client()`, `sort_orders_by_deadline()`,
`filter_orders_by_urgency()`, `show_orders()`.

### Stage

Атрибуты: `id`, `order`, `name`, `deadline`, `status`
(`planned` / `in_progress` / `done`).
Методы: `from_data()`, `to_dict()`, `change_status()`,
`deadline_status()`, `__str__()`.
Функции модуля: `next_stage_id()`, `remember_stage_id()`,
`add_stage()`, `find_stage_by_id()`, `find_stages_by_order()`,
`remove_stages_by_order()`, `update_stage()`,
`change_stage_status()`, `sort_stages_by_deadline()`,
`show_stages()`.

## Взаимодействие объектов

- `Order` хранит ссылки на объекты `Client` и `Designer`.
- `Stage` хранит ссылку на объект `Order`.
- Коллекции: `dict[str, Client]`, `dict[str, Designer]`,
  `list[Order]`, `list[Stage]`.

## Веб-интерфейс (ПР5)

### Структура Django-проекта

    designorders/
    ├── manage.py
    ├── requirements.txt
    ├── README.md
    ├── main.py                # консольная версия (ПР3)
    ├── storage.py             # JSON <-> объекты
    ├── utils.py               # консольный ввод/даты
    ├── designorders/          # пакет настроек Django
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py            # корневая маршрутизация + handler404
    │   ├── asgi.py
    │   └── wsgi.py
    ├── homepage/              # приложение: главная + 404
    ├── clients/               # приложение: клиенты
    ├── designers/             # приложение: дизайнеры
    ├── orders/                # приложение: заказы
    ├── stages/                # приложение: этапы
    ├── templates/             # HTML-шаблоны
    │   ├── base.html
    │   ├── 404.html
    │   ├── homepage/index.html
    │   ├── clients/…
    │   ├── designers/…
    │   ├── orders/…
    │   └── stages/…
    ├── models/                # классы предметной области (ПР3)
    ├── data/                  # JSON-хранилище
    └── tests/                 # pytest

### Страницы и URL

| URL | View | Результат |
|---|---|---|
| `/` | `homepage.views.index` | главная страница |
| `/clients/` | `clients.views.client_list` | список клиентов |
| `/clients/<str:client_id>/` | `clients.views.client_detail` | карточка клиента; 404, если нет |
| `/designers/` | `designers.views.designer_list` | список дизайнеров |
| `/designers/<str:designer_id>/` | `designers.views.designer_detail` | карточка дизайнера; 404, если нет |
| `/orders/` | `orders.views.order_list` | список заказов |
| `/orders/<int:order_id>/` | `orders.views.order_detail` | карточка заказа; 404, если нет |
| `/stages/` | `stages.views.stage_list` | все этапы |
| `/stages/order/<int:order_id>/` | `stages.views.stage_list` | этапы одного заказа |

Для несуществующего адреса срабатывает
`handler404 = 'homepage.views.page_not_found'`.

### Назначение view-функций

- `homepage.views.index` — главная страница с навигацией;
- `homepage.views.page_not_found` — обработчик 404;
- `clients.views.client_list` / `client_detail` — загрузка клиентов
  из JSON (`load_clients()`) и рендеринг;
- `designers.views.designer_list` / `designer_detail` — аналогично
  для дизайнеров (`load_designers()`);
- `orders.views.order_list` / `order_detail` — список заказов и карточка
  заказа (`load_orders()`, `find_order_by_id()`);
- `stages.views.stage_list` — этапы (все или для одного заказа)
  (`load_stages()`, `find_stages_by_order()`).

### HTML / CSS / Bootstrap

- `templates/base.html` — общий каркас: `<meta name="viewport">`,
  navbar, подключение Bootstrap 5.3 через CDN, блоки
  `{% block title %}` и `{% block content %}`;
- `templates/404.html` — страница ошибки 404;
- страницы предметной области: `clients/client_list.html`,
  `client_detail.html`; `designers/...`; `orders/...`;
  `stages/stage_list.html`;
- Bootstrap-классы: `container`, `navbar`, `list-group`, `card`,
  `badge`, `btn`.

## Формат хранения данных

- `data/clients.json` — словарь `id → {name, phone}`;
- `data/designers.json` — словарь `id → {name, specialization}`;
- `data/orders.json` — список словарей заказов;
- `data/stages.json` — список словарей этапов.

При загрузке данные JSON преобразуются в объекты классов.
При сохранении объекты преобразуются обратно в JSON.

## Запуск

Активировать виртуальное окружение и установить зависимости:

    pip install -r requirements.txt

Применить встроенные миграции Django и выполнить системную проверку:

    python manage.py migrate
    python manage.py check

Запустить development-сервер:

    python manage.py runserver

Открыть в браузере: <http://127.0.0.1:8000/>

Консольная версия (ПР3) по-прежнему работает:

    python main.py

## Тестирование и качество кода

    pytest -v
    flake8 . --extend-exclude=venv

## Git

Исходный код хранится в Git-репозитории. Коммиты, относящиеся к ПР5,
начинаются с метки `PR5:`.

    git status
    git add .
    git commit -m "PR5: add Django project and web pages"
    git push

## Текущее состояние и план развития

Реализовано (ПР5):

- Django-проект `designorders` и приложения `homepage`, `clients`,
  `designers`, `orders`, `stages`;
- маршрутизация двух уровней через `include()` и `app_name`;
- view-функции и HTML-шаблоны (Bootstrap 5.3);
- отображение данных ПР3 в веб-интерфейсе;
- обработка 404 (общий `handler404` + `404.html`);
- сохранена работоспособность консольного приложения `main.py`.

Планируется:

- перенос `Client`, `Designer`, `Order`, `Stage` в Django ORM;
- формы создания/редактирования заказов и этапов;
- отказ от JSON в пользу БД;
- регистрация и авторизация;
- API.