from datetime import date

import pytest
from django.db.models import Avg, Count, Sum

from clients.models import Client
from designers.models import Designer
from orders.models import Order
from stages.models import Stage


@pytest.mark.django_db
def test_create_client():
    client = Client.objects.create(name='Тест', phone='+7')
    assert Client.objects.count() == 1
    assert str(client) == 'Тест (+7)'


@pytest.mark.django_db
def test_order_relations():
    client = Client.objects.create(name='Клиент', phone='')
    designer = Designer.objects.create(name='Дизайнер', specialization='LOGO')
    order = Order.objects.create(
        client=client,
        designer=designer,
        design_type='LOGO',
        price=1000,
        is_urgent=True,
        deadline=date(2026, 12, 31),
    )
    assert order.client.name == 'Клиент'
    assert order.designer.name == 'Дизайнер'
    assert client.orders.count() == 1
    assert designer.orders.count() == 1


@pytest.mark.django_db
def test_stage_cascade():
    client = Client.objects.create(name='К', phone='')
    designer = Designer.objects.create(name='Д', specialization='')
    order = Order.objects.create(
        client=client, designer=designer, design_type='LOGO',
        price=100, deadline=date(2026, 12, 31),
    )
    Stage.objects.create(order=order, name='Этап', deadline=date(2026, 1, 1))
    assert order.stages.count() == 1
    order.delete()
    assert Stage.objects.count() == 0  # CASCADE


@pytest.mark.django_db
def test_orm_queries():
    c = Client.objects.create(name='ООО', phone='')
    d = Designer.objects.create(name='Виктория', specialization='LOGO')
    Order.objects.create(
        client=c, designer=d, design_type='LOGO',
        price=10000, is_urgent=True, deadline=date(2026, 12, 31),
    )
    Order.objects.create(
        client=c, designer=d, design_type='BANNER',
        price=5000, is_urgent=False, deadline=date(2026, 11, 1),
    )

    assert Order.objects.count() == 2
    assert Order.objects.filter(is_urgent=True).count() == 1
    assert Order.objects.filter(client__name__icontains='ООО').count() == 2
    assert Order.objects.exclude(is_urgent=True).count() == 1

    stats = Order.objects.aggregate(total=Sum('price'), avg=Avg('price'))
    assert stats['total'] == 15000
    assert stats['avg'] == 7500

    by_designer = Designer.objects.annotate(
        n=Count('orders'), total=Sum('orders__price')
    ).get(pk=d.pk)
    assert by_designer.n == 2
    assert by_designer.total == 15000