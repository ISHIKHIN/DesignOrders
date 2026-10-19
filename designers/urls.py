from django.urls import path
from . import views

app_name = 'designers'

urlpatterns = [
    path('', views.designer_list, name='list'),
    path('<str:designer_id>/', views.designer_detail, name='detail'),
]