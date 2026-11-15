from orders.models import Order
from stages.models import Stage


def site_info(request):
    return {
        'site_name': 'DesignOrders',
        'total_orders': Order.objects.count(),
        'active_stages': Stage.objects.active().count(),
    }