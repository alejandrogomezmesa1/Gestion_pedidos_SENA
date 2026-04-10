from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cliente

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    direccion = serializers.CharField(required=False, allow_blank=True)
    telefono = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'direccion', 'telefono')

    def create(self, validated_data):
        direccion = validated_data.pop('direccion', '')
        telefono = validated_data.pop('telefono', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Cliente.objects.create(
            nombre_cliente=user.username,
            email=user.email,
            direccion=direccion,
            telefono=telefono
        )
        return user
