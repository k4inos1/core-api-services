from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('equipos/', include('equipos.urls')),
    path('entregables/', include('entregables.urls')),
    path('api/', include('api.urls')),
]
