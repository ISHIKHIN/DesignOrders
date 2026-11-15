from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Client


def client_list(request):
    query = request.GET.get('q', '').strip()
    clients = Client.objects.all()

    if query:
        clients = clients.filter(
            Q(name__icontains=query) | Q(phone__icontains=query)
        )

    clients = clients.annotate(orders_count=Count('orders'))

    return render(request, 'clients/client_list.html', {
        'clients': clients,
        'query': query,
    })


def client_detail(request, slug):
    client = get_object_or_404(Client, slug=slug)
    orders = client.orders.select_related('designer').all()
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'orders': orders,
    })