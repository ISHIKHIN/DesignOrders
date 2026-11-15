import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date

from clients.models import Client
from designers.models import Designer
from orders.models import Order
from stages.models import Stage

DATA_DIR = Path('data')


def _load(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


class Command(BaseCommand):
    help = 'Перенос данных из JSON (ПР3/ПР7) в Django ORM'

    def handle(self, *args, **options):
        raw = _load('clients.json') or {}
        client_map = {}
        for old_id, data in raw.items():
            obj, _ = Client.objects.get_or_create(
                name=data.get('name', ''),
                defaults={'phone': data.get('phone', '')},
            )
            client_map[str(old_id)] = obj
        self.stdout.write(f'Клиентов: {Client.objects.count()}')

        raw = _load('designers.json') or {}
        designer_map = {}
        for old_id, data in raw.items():
            obj, _ = Designer.objects.get_or_create(
                name=data.get('name', ''),
                defaults={'specialization': data.get('specialization', '')},
            )
            designer_map[str(old_id)] = obj
        self.stdout.write(f'Дизайнеров: {Designer.objects.count()}')

        raw = _load('orders.json') or []
        order_map = {}
        for data in raw:
            client = client_map.get(str(data.get('client_id')))
            designer = designer_map.get(str(data.get('designer_id')))
            if not client or not designer:
                self.stdout.write(self.style.WARNING(
                    f'Пропущен заказ {data.get("order_id")}: '
                    f'нет клиента/дизайнера'
                ))
                continue

            deadline = data.get('deadline')
            if isinstance(deadline, str):
                deadline = parse_date(deadline)

            order, _ = Order.objects.get_or_create(
                client=client,
                designer=designer,
                design_type=data.get('design_type', ''),
                deadline=deadline,
                defaults={
                    'price': data.get('price', 0),
                    'is_urgent': bool(data.get('is_urgent', False)),
                },
            )
            order_map[str(data.get('order_id'))] = order
        self.stdout.write(f'Заказов: {Order.objects.count()}')

        raw = _load('stages.json') or []
        for data in raw:
            order = order_map.get(str(data.get('order_id')))
            if not order:
                self.stdout.write(self.style.WARNING(
                    f'Пропущен этап {data.get("stage_id")}: нет заказа'
                ))
                continue

            deadline = data.get('deadline')
            if isinstance(deadline, str):
                deadline = parse_date(deadline)

            Stage.objects.get_or_create(
                order=order,
                name=data.get('name', ''),
                deadline=deadline,
                defaults={'status': data.get('status', Stage.STATUS_PLANNED)},
            )
        self.stdout.write(f'Этапов: {Stage.objects.count()}')

        self.stdout.write(self.style.SUCCESS('Импорт завершён.'))
