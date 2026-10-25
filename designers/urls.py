from django.urls import path
from . import views

app_name = 'designers'

urlpatterns = [
    path('', views.designer_list, name='list'),
    path('<int:designer_id>/', views.designer_detail, name='detail'),
]