from django.urls import path

from . import views

app_name = 'stages'

urlpatterns = [
    path('', views.stage_list, name='list'),
    path(
        'order/<int:order_id>/',
        views.stage_list,
        name='list_by_order',
    ),
    path(
        '<int:stage_id>/',
        views.stage_detail,
        name='detail',
    ),
]