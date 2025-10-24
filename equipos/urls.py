from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipos_list, name='equipos-list'),
]
