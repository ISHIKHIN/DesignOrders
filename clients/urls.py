from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list, name='list'),
    path('<str:client_id>/', views.client_detail, name='detail'),
]