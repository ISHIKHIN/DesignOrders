from django.shortcuts import render
from db.database import get_connection


def client_list(request):
    conn = get_connection()
    clients = conn.execute(
        "SELECT id, name, phone FROM clients ORDER BY name;"
    ).fetchall()
    conn.close()
    return render(request, 'clients/client_list.html', {'clients': clients})


def client_detail(request, client_id):
    conn = get_connection()
    client = conn.execute(
        "SELECT id, name, phone FROM clients WHERE id = ?;",
        (client_id,)
    ).fetchone()
    conn.close()

    if client is None:
        return render(
            request,
            '404.html',
            {'message': f'Клиент с ID {client_id} не найден'},
            status=404
        )

    return render(request, 'clients/client_detail.html', {'client': client})