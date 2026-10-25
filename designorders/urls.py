from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('clients/', include('clients.urls')),
    path('designers/', include('designers.urls')),
    path('orders/', include('orders.urls')),
    path('stages/', include('stages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')

handler404 = 'homepage.views.page_not_found'