from django.shortcuts import render
from storage import load_clients, load_designers, load_orders, load_stages
from models.orders import find_order_by_id
from models.stages import find_stages_by_order

def stage_list(request, order_id=None):
    clients = load_clients()
    designers = load_designers()
    orders = load_orders(clients, designers)
    stages = load_stages(orders)

    order = None
    if order_id:
        order = find_order_by_id(orders, order_id)
        if order:
            stages = find_stages_by_order(stages, order)

    return render(request, 'stages/stage_list.html', {'stages': stages, 'order': order})