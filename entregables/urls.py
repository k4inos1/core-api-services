from django.urls import path
from . import views

urlpatterns = [
    # Index
    path('', views.index, name='index'),
    
    # Vehículos CRUD
    path('vehiculos/', views.vehiculo_list, name='vehiculo_list'),
    path('vehiculos/crear/', views.vehiculo_create, name='vehiculo_create'),
    path('vehiculos/<int:pk>/editar/', views.vehiculo_update, name='vehiculo_update'),
    path('vehiculos/<int:pk>/eliminar/', views.vehiculo_delete, name='vehiculo_delete'),
    
    # Operarios CRUD
    path('operarios/', views.operario_list, name='operario_list'),
    path('operarios/crear/', views.operario_create, name='operario_create'),
    path('operarios/<int:pk>/editar/', views.operario_update, name='operario_update'),
    path('operarios/<int:pk>/eliminar/', views.operario_delete, name='operario_delete'),
    
    # Faenas CRUD
    path('faenas/', views.faena_list, name='faena_list'),
    path('faenas/crear/', views.faena_create, name='faena_create'),
    path('faenas/<int:pk>/', views.faena_detail, name='faena_detail'),
    path('faenas/<int:pk>/editar/', views.faena_update, name='faena_update'),
    path('faenas/<int:pk>/eliminar/', views.faena_delete, name='faena_delete'),
]
