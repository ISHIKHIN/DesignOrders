from django.http import Http404
from django.shortcuts import render
from db.database import get_connection

def client_list(request):
    conn = get_connection()
    clients = conn.execute("SELECT id, name, phone FROM clients ORDER BY name;").fetchall()
    conn.close()
    return render(request, 'clients/client_list.html', {'clients': clients})

def client_detail(request, client_id):
    conn = get_connection()
    client = conn.execute("SELECT id, name, phone FROM clients WHERE id = ?;", (client_id,)).fetchone()
    conn.close()
    if client is None:
        request.not_found_message = f'Клиент с ID {client_id} не найден'
        raise Http404("Клиент не найден")
    return render(request, 'clients/client_detail.html', {'client': client})