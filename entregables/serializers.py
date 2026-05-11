from rest_framework import serializers

from .models import Faena, Mantencion, Operario, RegistroIncidente, Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    requiere_mantencion = serializers.BooleanField(read_only=True)

    class Meta:
        model = Vehiculo
        fields = '__all__'


class OperarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operario
        fields = '__all__'


class MantencionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantencion
        fields = '__all__'


class FaenaSerializer(serializers.ModelSerializer):
    duracion_dias = serializers.IntegerField(read_only=True)

    class Meta:
        model = Faena
        fields = '__all__'


class RegistroIncidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroIncidente
        fields = '__all__'
