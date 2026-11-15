from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import get_object_or_404, render

from clients.models import Client
from designers.models import Designer

from .models import Order


SORT_FIELDS = {
    'deadline': {'field': 'deadline', 'label': 'Дедлайн (сначала ранние)'},
    '-deadline': {'field': '-deadline', 'label': 'Дедлайн (сначала поздние)'},
    'price': {'field': 'price', 'label': 'Цена (сначала дешевле)'},
    '-price': {'field': '-price', 'label': 'Цена (сначала дороже)'},
    'client': {'field': 'client__name', 'label': 'Клиент (А-Я)'},
    'designer': {'field': 'designer__name', 'label': 'Дизайнер (А-Я)'},
}

PAGE_SIZE = 5


def _parse_date(value: str):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None


def _parse_price(value: str):
    """Парсит цену: '10000', '10000.50', '10000,50' → float."""
    if not value:
        return None
    try:
        return float(value.replace(',', '.').strip())
    except (ValueError, TypeError):
        return None


def order_list(request):
    orders = Order.objects.select_related('client', 'designer')

    query = request.GET.get('q', '').strip()
    if query:
        orders = orders.filter(
            Q(design_type__icontains=query)
            | Q(client__name__icontains=query)
            | Q(designer__name__icontains=query)
        )

    client_id = request.GET.get('client', '').strip()
    if client_id.isdigit():
        orders = orders.filter(client_id=int(client_id))

    designer_id = request.GET.get('designer', '').strip()
    if designer_id.isdigit():
        orders = orders.filter(designer_id=int(designer_id))

    urgent = request.GET.get('urgent', '').strip()
    if urgent == '1':
        orders = orders.filter(is_urgent=True)
    elif urgent == '0':
        orders = orders.filter(is_urgent=False)

    min_price = _parse_price(request.GET.get('min_price', ''))
    if min_price is not None:
        orders = orders.filter(price__gte=min_price)

    max_price = _parse_price(request.GET.get('max_price', ''))
    if max_price is not None:
        orders = orders.filter(price__lte=max_price)

    date_from = _parse_date(request.GET.get('date_from', ''))
    if date_from:
        orders = orders.filter(deadline__gte=date_from)

    date_to = _parse_date(request.GET.get('date_to', ''))
    if date_to:
        orders = orders.filter(deadline__lte=date_to)

    hide_done = request.GET.get('hide_done', '').strip()
    if hide_done == '1':
        orders = orders.exclude(stages__status='done')

    sort = request.GET.get('sort', 'deadline')
    sort_config = SORT_FIELDS.get(sort, SORT_FIELDS['deadline'])
    orders = orders.order_by(sort_config['field'])

    stats = orders.aggregate(
        total=Sum('price'),
        avg=Avg('price'),
        count=Count('id'),
    )

    paginator = Paginator(orders, PAGE_SIZE)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    params = request.GET.copy()
    params.pop('page', None)
    querystring = params.urlencode()

    return render(request, 'orders/order_list.html', {
        'page_obj': page_obj,
        'orders': page_obj.object_list,
        'stats': stats,
        'clients': Client.objects.all(),
        'designers': Designer.objects.all(),
        'sort_fields': SORT_FIELDS.items(),
        'current_sort': sort,
        'query': query,
        'querystring': querystring,
    })


def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('client', 'designer'),
        pk=order_id,
    )
    stages = order.stages.all()
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'stages': stages,
    })


def order_statistics(request):
    by_designer = (
        Designer.objects
        .annotate(
            orders_count=Count('orders'),
            total_price=Sum('orders__price'),
        )
        .order_by('-total_price')
    )

    total_count = Order.objects.count()
    urgent_count = Order.objects.filter(is_urgent=True).count()

    return render(request, 'orders/order_statistics.html', {
        'by_designer': by_designer,
        'total_count': total_count,
        'urgent_count': urgent_count,
    })