from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from orders.models import Order
from .models import Stage


def stage_list(request, order_id=None):
    order = None
    stages = Stage.objects.select_related('order')

    if order_id is not None:
        order = get_object_or_404(Order, pk=order_id)
        stages = stages.filter(order=order)

    status = request.GET.get('status', '').strip()
    if status in dict(Stage.Status.choices):
        stages = stages.filter(status=status)

    query = request.GET.get('q', '').strip()
    if query:
        stages = stages.filter(Q(name__icontains=query))

    stages = stages.order_by('deadline')

    return render(request, 'stages/stage_list.html', {
        'stages': stages,
        'order': order,
        'statuses': Stage.Status.choices,
        'current_status': status,
        'query': query,
    })


def stage_detail(request, stage_id):
    stage = get_object_or_404(
        Stage.objects.select_related('order'),
        pk=stage_id,
    )
    return render(request, 'stages/stage_detail.html', {'stage': stage})