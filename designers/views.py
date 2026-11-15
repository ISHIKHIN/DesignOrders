from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import get_object_or_404, render

from .models import Designer


def designer_list(request):
    query = request.GET.get('q', '').strip()
    designers = Designer.objects.all()

    if query:
        designers = designers.filter(
            Q(name__icontains=query)
            | Q(specialization__icontains=query)
        )

    designers = designers.annotate(
        orders_count=Count('orders'),
        total_price=Sum('orders__price'),
    )

    return render(request, 'designers/designer_list.html', {
        'designers': designers,
        'query': query,
    })


def designer_detail(request, designer_id):
    designer = get_object_or_404(Designer, pk=designer_id)
    orders = designer.orders.select_related('client').all()
    stats = designer.orders.aggregate(
        total=Sum('price'),
        avg=Avg('price'),
        count=Count('id'),
    )
    return render(request, 'designers/designer_detail.html', {
        'designer': designer,
        'orders': orders,
        'stats': stats,
    })