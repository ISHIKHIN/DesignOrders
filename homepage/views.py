from django.db.models import Count, Q
from django.shortcuts import render

from clients.models import Client
from designers.models import Designer
from orders.models import Order
from stages.models import Stage


def index(request):
    context = {
        'orders_count': Order.objects.count(),
        'clients_count': Client.objects.count(),
        'designers_count': Designer.objects.count(),
        'urgent_count': Order.objects.filter(is_urgent=True).count(),
        'recent_orders': (
            Order.objects
            .select_related('client', 'designer')
            .order_by('-created_at')[:5]
        ),
        'stage_stats': Stage.objects.aggregate(
            planned=Count('id', filter=Q(status=Stage.Status.PLANNED)),
            in_progress=Count('id', filter=Q(status=Stage.Status.IN_PROGRESS)),
            done=Count('id', filter=Q(status=Stage.Status.DONE)),
        ),
        'order_stats': Order.objects.aggregate(
            new=Count('id', filter=Q(status=Order.Status.NEW)),
            in_progress=Count('id', filter=Q(status=Order.Status.IN_PROGRESS)),
            done=Count('id', filter=Q(status=Order.Status.DONE)),
            cancelled=Count('id', filter=Q(status=Order.Status.CANCELLED)),
        ),
    }
    return render(request, 'homepage/index.html', context)


def page_not_found(request, exception=None):
    message = getattr(request, 'not_found_message', 'Страница не найдена')
    return render(request, '404.html', {'message': message}, status=404)