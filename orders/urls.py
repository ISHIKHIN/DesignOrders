from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('search/', views.order_search, name='search'),
    path('statistics/', views.order_statistics, name='statistics'),
]