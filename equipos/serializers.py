from rest_framework import serializers

from .models import CambioEquipo, Equipo


class CambioEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CambioEquipo
        fields = '__all__'


class EquipoSerializer(serializers.ModelSerializer):
    cambios = CambioEquipoSerializer(many=True, read_only=True)

    class Meta:
        model = Equipo
        fields = '__all__'
