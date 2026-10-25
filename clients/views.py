from django.http import Http404
from django.shortcuts import render

from storage import load_clients


def client_list(request):
    clients = load_clients()
    return render(
        request,
        'clients/client_list.html',
        {'clients': clients.values()},
    )


def client_detail(request, client_id):
    clients = load_clients()
    client = clients.get(client_id)
    if client is None:
        request.not_found_message = f'Клиент с ID {client_id} не найден'
        raise Http404("Клиент не найден")
    return render(
        request,
        'clients/client_detail.html',
        {'client': client},
    )