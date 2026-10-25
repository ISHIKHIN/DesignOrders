from django.http import Http404
from django.shortcuts import render

from models.orders import find_order_by_id
from models.stages import find_stage_by_id, find_stages_by_order
from storage import (
    load_clients,
    load_designers,
    load_orders,
    load_stages,
)


def stage_list(request, order_id=None):
    clients = load_clients()
    designers = load_designers()
    orders = load_orders(clients, designers)
    stages = load_stages(orders)

    order = None
    if order_id is not None:
        order = find_order_by_id(orders, order_id)
        if order is None:
            request.not_found_message = f'Заказ №{order_id} не найден'
            raise Http404("Заказ не найден")
        stages = find_stages_by_order(stages, order)

    return render(
        request,
        'stages/stage_list.html',
        {'stages': stages, 'order': order},
    )


def stage_detail(request, stage_id):
    clients = load_clients()
    designers = load_designers()
    orders = load_orders(clients, designers)
    stages = load_stages(orders)
    stage = find_stage_by_id(stages, stage_id)
    if stage is None:
        request.not_found_message = f'Этап №{stage_id} не найден'
        raise Http404("Этап не найден")
    return render(
        request,
        'stages/stage_detail.html',
        {'stage': stage},
    )