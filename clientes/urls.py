from django.shortcuts import render
from django.urls import path
from . import views
# Create your views here.

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='listar_clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('<int:pk>/', views.ver_cliente, name='ver_cliente'),
    path('editar/<int:pk>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('exportar/pdf/', views.exportar_clientes_pdf, name='exportar_clientes_pdf'),
    path('exportar/excel/', views.exportar_clientes_excel, name='exportar_clientes_excel'),
]               