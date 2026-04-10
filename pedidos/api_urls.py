from django.urls import path
from rest_framework import generics
from .models import Pedido
from .serializers import PedidoSerializer

class PedidoListCreateView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class PedidoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

urlpatterns = [
    path('', PedidoListCreateView.as_view(), name='pedido-list-create'),
    path('<int:pk>/', PedidoRetrieveUpdateDestroyView.as_view(), name='pedido-detail'),
]
