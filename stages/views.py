from django.shortcuts import render
from db.database import get_connection
from homepage.views import page_not_found


def stage_list(request, order_id=None):
    conn = get_connection()
    order = None

    if order_id is not None:
        order = conn.execute(
            "SELECT id, design_type FROM orders WHERE id = ?;",
            (order_id,)
        ).fetchone()

        if order is None:
            conn.close()
            request.not_found_message = f'Заказ №{order_id} не найден'
            return page_not_found(request, None)

        stages = conn.execute(
            "SELECT id, name, deadline, status, order_id "
            "FROM stages WHERE order_id = ? ORDER BY deadline;",
            (order_id,)
        ).fetchall()
    else:
        stages = conn.execute("""
            SELECT s.id, s.name, s.deadline, s.status, s.order_id, o.design_type
            FROM stages s
            JOIN orders o ON s.order_id = o.id
            ORDER BY s.deadline;
        """).fetchall()

    conn.close()
    return render(request, 'stages/stage_list.html', {'stages': stages, 'order': order})


def stage_detail(request, stage_id):
    conn = get_connection()
    stage = conn.execute("""
        SELECT s.id, s.name, s.deadline, s.status, s.order_id, o.design_type
        FROM stages s
        JOIN orders o ON s.order_id = o.id
        WHERE s.id = ?;
    """, (stage_id,)).fetchone()
    conn.close()

    if stage is None:
        request.not_found_message = f'Этап №{stage_id} не найден'
        return page_not_found(request, None)

    return render(request, 'stages/stage_detail.html', {'stage': stage})