from django import forms
from .models import DetallePedido

class DetallePedidoForm(forms.ModelForm):

    class Meta:
        model = DetallePedido
        fields = ['pedidoId', 'productoId', 'cantidad']
        
        widgets = {
            'pedidoId': forms.Select(attrs={
                'class': 'form-control',
            }),

            'productoId': forms.Select(attrs={
                'class': 'form-control',
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cantidad del producto'
            }),

        }