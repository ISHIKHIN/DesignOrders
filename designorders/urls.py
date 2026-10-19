from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('clients/', include('clients.urls')),
    path('designers/', include('designers.urls')),
    path('orders/', include('orders.urls')),
    path('stages/', include('stages.urls')),
]

handler404 = 'homepage.views.page_not_found'