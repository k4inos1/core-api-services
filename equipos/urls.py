from django.urls import path

from .views import lista_equipos

urlpatterns = [
    path('', lista_equipos, name='equipos-list'),
]
