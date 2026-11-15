from django.shortcuts import render

from clients.models import Client
from designers.models import Designer
from orders.models import Order


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
    }
    return render(request, 'homepage/index.html', context)


def page_not_found(request, exception=None):
    message = getattr(request, 'not_found_message', 'Страница не найдена')
    return render(request, '404.html', {'message': message}, status=404)