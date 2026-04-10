from django.urls import path
from rest_framework import generics
from .models import Producto
from .serializers import ProductoSerializer

class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

urlpatterns = [
    path('', ProductoListCreateView.as_view(), name='producto-list-create'),
    path('<int:pk>/', ProductoRetrieveUpdateDestroyView.as_view(), name='producto-detail'),
]
