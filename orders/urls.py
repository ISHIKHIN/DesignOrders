from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('free-designers/', views.free_designers, name='free_designers'),
    path('statistics/', views.order_statistics, name='statistics'),
    path('<int:order_id>/', views.order_detail, name='detail'),
]