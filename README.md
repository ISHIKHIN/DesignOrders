## ПР9. Переход на Django ORM

### Что изменилось

- Слой доступа к данным переведён с `sqlite3` (`db/database.py`) на Django ORM.
- Созданы модели: `clients.Client`, `designers.Designer`,
  `orders.Order`, `stages.Stage`.
- Связи: `Order.client → Client`, `Order.designer → Designer` (FK, `PROTECT`,
  `related_name='orders'`); `Stage.order → Order` (FK, `CASCADE`,
  `related_name='stages'`).
- Созданы и применены миграции.
- Данные перенесены из JSON management-командой
  `python manage.py load_from_json`.
- Консольная версия ПР3 (`main.py`) и её тесты сохранены и работают
  на пакете `models/` (не пересекается с Django-моделями).

### ORM-запросы в проекте (22 выражения)

| Категория | Пример |
|---|---|
| Получение набора | `Client.objects.all()` |
| Получение одного | `get_object_or_404(Order, pk=...)` |
| Фильтр по 1 условию | `Order.objects.filter(is_urgent=True)` |
| Фильтр по нескольким | `filter(client_id=...).filter(urgent=...)` |
| Фильтр по связанному | `filter(client__name__icontains=q)` |
| Исключение | `exclude(stages__status='done')` |
| Поиск | `Q(design_type__icontains=q) | Q(client__name__icontains=q)` |
| Сортировка | `order_by('-price')`, `order_by('deadline')` |
| Связи + оптимизация | `select_related('client', 'designer')` |
| Сокращённый набор | `values('id', 'design_type', 'client__name')` |
| Агрегирование | `aggregate(total=Sum('price'), avg=Avg('price'))` |
| Аннотирование | `annotate(Count('orders'), Sum('orders__price'))` |
| Пагинация | `Paginator(orders, 5)` + `page_obj` в шаблоне |
| Ограничение | `order_by('-created_at')[:5]` |

### Запуск

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py load_from_json
python manage.py check
python manage.py runserver