from datetime import date

import pytest
from django.db.models import Count, Q
from django.test import Client as DjangoClient

from clients.models import Client
from designers.models import Designer
from orders.models import Order
from stages.models import Stage


@pytest.mark.django_db
def test_stage_status_choices():
    assert Stage.Status.PLANNED == 'planned'
    assert Stage.Status.IN_PROGRESS == 'in_progress'
    assert Stage.Status.DONE == 'done'


@pytest.mark.django_db
def test_stage_queryset_active():
    c = Client.objects.create(name='К', phone='')
    d = Designer.objects.create(name='Д', specialization='')
    o = Order.objects.create(
        client=c, designer=d, design_type='LOGO',
        price=100, deadline=date(2026, 12, 31),
    )
    Stage.objects.create(order=o, name='A', deadline=date(2026, 1, 1), status=Stage.Status.DONE)
    Stage.objects.create(order=o, name='B', deadline=date(2026, 2, 1), status=Stage.Status.PLANNED)

    assert Stage.objects.active().count() == 1
    assert Stage.objects.planned().count() == 1
    assert Stage.objects.done().count() == 1


@pytest.mark.django_db
def test_order_status_aggregate():
    c = Client.objects.create(name='К', phone='')
    d = Designer.objects.create(name='Д', specialization='')
    Order.objects.create(
        client=c, designer=d, design_type='LOGO',
        price=100, deadline=date(2026, 12, 31), status=Order.Status.NEW,
    )
    Order.objects.create(
        client=c, designer=d, design_type='BANNER',
        price=200, deadline=date(2026, 12, 1), status=Order.Status.DONE,
    )

    stats = Order.objects.aggregate(
        new=Count('id', filter=Q(status=Order.Status.NEW)),
        done=Count('id', filter=Q(status=Order.Status.DONE)),
    )
    assert stats['new'] == 1
    assert stats['done'] == 1


@pytest.mark.django_db
def test_get_absolute_url():
    c = Client.objects.create(name='ООО Компания', phone='')
    assert c.slug
    assert c.get_absolute_url() == f'/clients/{c.slug}/'


@pytest.mark.django_db
def test_free_designers():
    c = Client.objects.create(name='К', phone='')
    d1 = Designer.objects.create(name='D1', specialization='')
    d2 = Designer.objects.create(name='D2', specialization='')

    Order.objects.create(
        client=c, designer=d1, design_type='LOGO',
        price=100, deadline=date(2026, 12, 31), status=Order.Status.NEW,
    )

    client = DjangoClient()
    response = client.get('/orders/free-designers/', {'date': '2026-12-31'})

    assert response.status_code == 200
    designers = list(response.context['designers'])

    assert d2 in designers
    assert d1 not in designers