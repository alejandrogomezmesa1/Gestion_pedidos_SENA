from django.urls import path
from . import views


urlpatterns = [
    # Ruta raíz del módulo "pedidos".
    # Cuando el usuario entra a /pedidos/, Django ejecuta la función listar_pedidos()
    path('', views.PedidoListView.as_view(), name='listar_pedidos'),
    # Ruta para crear un nuevo pedido.
    path('crear/', views.crear_pedido, name='crear_pedido'),
    # Ruta para ver el detalle de un pedido específico.
    path('<int:pk>/', views.ver_pedido, name='ver_pedido'),
     # Ruta para editar un pedido existente.
    # URL: /pedidos/editar/5/
    path('editar/<int:pk>/', views.actualizar_pedido, name='actualizar_pedido'),
     # Ruta para eliminar un pedido existente
    path('eliminar/<int:pk>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('exportar/pdf/', views.exportar_pedidos_pdf, name='exportar_pedidos_pdf'),
    path('exportar/excel/', views.exportar_pedidos_excel, name='exportar_pedidos_excel'),
]
