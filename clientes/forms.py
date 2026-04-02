from django.shortcuts import render
from .models import Cliente
from django import forms

# Create your views here.

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_cliente', 'email', 'dirección', 'teléfono']
        
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el email del cliente'
            }),
            'dirección': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección del cliente'
            }),
            'teléfono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el teléfono del cliente'
            })
        }
        