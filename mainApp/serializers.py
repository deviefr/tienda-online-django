from rest_framework import serializers
from .models import Insumo, Pedido

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ['token', 'creado']

class PedidoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['cliente_nombre', 'cliente_contacto', 'producto', 'descripcion', 'plataforma', 'fecha_solicitud', 'estado', 'estado_pago', 'total']
        read_only_fields = ['token', 'creado']