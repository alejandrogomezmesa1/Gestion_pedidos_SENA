from django.urls import path
from rest_framework import generics
from .models import DetallePedido
from .serializers import DetallePedidoSerializer

class DetallePedidoListCreateView(generics.ListCreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class DetallePedidoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

urlpatterns = [
    path('', DetallePedidoListCreateView.as_view(), name='detallepedido-list-create'),
    path('<int:pk>/', DetallePedidoRetrieveUpdateDestroyView.as_view(), name='detallepedido-detail'),
]
