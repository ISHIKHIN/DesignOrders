from django.http import Http404
from django.shortcuts import render
from db.database import get_connection


def order_list(request):
    conn = get_connection()
    orders = conn.execute("""
                          SELECT o.id,
                                 o.design_type,
                                 o.price,
                                 o.is_urgent,
                                 o.deadline,
                                 c.name AS client_name,
                                 d.name AS designer_name
                          FROM orders o
                                   JOIN clients c ON o.client_id = c.id
                                   JOIN designers d ON o.designer_id = d.id
                          ORDER BY o.deadline;
                          """).fetchall()
    conn.close()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, order_id):
    conn = get_connection()
    order = conn.execute("""
                         SELECT o.id,
                                o.design_type,
                                o.price,
                                o.is_urgent,
                                o.deadline,
                                c.name AS client_name,
                                d.name AS designer_name
                         FROM orders o
                                  JOIN clients c ON o.client_id = c.id
                                  JOIN designers d ON o.designer_id = d.id
                         WHERE o.id = ?;
                         """, (order_id,)).fetchone()
    conn.close()
    if order is None:
        request.not_found_message = f'Заказ №{order_id} не найден'
        raise Http404("Заказ не найден")
    return render(request, 'orders/order_detail.html', {'order': order})


def order_search(request):
    min_price = request.GET.get('min_price')
    results = []
    if min_price:
        conn = get_connection()
        results = conn.execute(
            "SELECT id, design_type, price, deadline FROM orders WHERE price >= ? ORDER BY price DESC;",
            (float(min_price),)
        ).fetchall()
        conn.close()
    return render(request, 'orders/order_search.html', {'orders': results, 'min_price': min_price})


def order_statistics(request):
    conn = get_connection()

    by_designer = conn.execute("""
                               SELECT d.name AS designer_name, COUNT(o.id) AS orders_count, SUM(o.price) AS total_price
                               FROM designers d
                                        LEFT JOIN orders o ON o.designer_id = d.id
                               GROUP BY d.id, d.name
                               ORDER BY total_price DESC;
                               """).fetchall()

    total = conn.execute("SELECT COUNT(*) AS c FROM orders;").fetchone()
    urgent = conn.execute("SELECT COUNT(*) AS c FROM orders WHERE is_urgent = 1;").fetchone()
    conn.close()

    return render(request, 'orders/order_statistics.html', {
        'by_designer': by_designer,
        'total_count': total['c'],
        'urgent_count': urgent['c'],
    })