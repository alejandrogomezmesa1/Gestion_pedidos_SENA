from django.shortcuts import render
from .models import Cliente
from django import forms

# Create your views here.

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_cliente', 'email', 'direccion', 'telefono']
        
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el email del cliente'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección del cliente'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono del cliente'
            })
        }
