from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['clienteId', 'estado']
        
        widgets = {
            'clienteId': forms.Select(attrs={
                'class': 'form-control',
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            })
        }


