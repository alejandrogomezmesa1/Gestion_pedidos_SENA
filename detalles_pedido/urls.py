from django.urls import path
from . import views

urlpatterns = [
    path('', views.DetallePedidoListView.as_view(), name='listar_detalle_pedidos'),
    path('crear/', views.crear_detalle_pedido, name='crear_detalle_pedido'),
    path('<int:pk>/', views.ver_detalle_pedido, name='ver_detalle_pedido'),
    path('editar/<int:pk>/', views.actualizar_detalle_pedido, name='actualizar_detalle_pedido'),
    path('eliminar/<int:pk>/', views.eliminar_detalle_pedido, name='eliminar_detalle_pedido'),
    path('exportar/pdf/', views.exportar_detalles_pdf, name='exportar_detalles_pdf'),
    path('exportar/excel/', views.exportar_detalles_excel, name='exportar_detalles_excel'),
]