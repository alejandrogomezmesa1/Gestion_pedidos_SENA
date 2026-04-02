from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='listar_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('<int:pk>/', views.ver_producto, name='ver_producto'),
    path('editar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('exportar/pdf/', views.exportar_productos_pdf, name='exportar_productos_pdf'),
    path('exportar/excel/', views.exportar_productos_excel, name='exportar_productos_excel'),
]