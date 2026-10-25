from django.http import Http404
from django.shortcuts import render

from models.orders import find_order_by_id
from storage import load_clients, load_designers, load_orders


def order_list(request):
    clients = load_clients()
    designers = load_designers()
    orders = load_orders(clients, designers)
    return render(
        request,
        'orders/order_list.html',
        {'orders': orders},
    )


def order_detail(request, order_id):
    clients = load_clients()
    designers = load_designers()
    orders = load_orders(clients, designers)
    order = find_order_by_id(orders, order_id)
    if order is None:
        request.not_found_message = f'Заказ №{order_id} не найден'
        raise Http404("Заказ не найден")
    return render(
        request,
        'orders/order_detail.html',
        {'order': order},
    )