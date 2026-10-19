from django.shortcuts import render
from storage import load_clients

def client_list(request):
    clients = load_clients()
    return render(request, 'clients/client_list.html', {'clients': clients.values()})

def client_detail(request, client_id):
    clients = load_clients()
    client = clients.get(client_id)
    return render(request, 'clients/client_detail.html', {'client': client})