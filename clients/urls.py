from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client_list, name='list'),
    path('<slug:slug>/', views.client_detail, name='detail'),
]