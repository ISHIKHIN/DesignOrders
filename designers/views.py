from django.shortcuts import render
from db.database import get_connection
from homepage.views import page_not_found


def designer_list(request):
    conn = get_connection()
    designers = conn.execute(
        "SELECT id, name, specialization FROM designers ORDER BY name;"
    ).fetchall()
    conn.close()
    return render(request, 'designers/designer_list.html', {'designers': designers})


def designer_detail(request, designer_id):
    conn = get_connection()
    designer = conn.execute(
        "SELECT id, name, specialization FROM designers WHERE id = ?;",
        (designer_id,)
    ).fetchone()
    conn.close()

    if designer is None:
        request.not_found_message = f'Дизайнер с ID {designer_id} не найден'
        return page_not_found(request, None)

    return render(request, 'designers/designer_detail.html', {'designer': designer})