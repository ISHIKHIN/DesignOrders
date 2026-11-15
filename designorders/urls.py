from django.conf import settings
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

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

handler404 = 'homepage.views.page_not_found'