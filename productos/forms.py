from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'precio', 'unidades_stock']
        
        widgets = {
            'nombre_producto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el precio del producto'
            }),
            'unidades_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese las unidades en stock'
            })
        }