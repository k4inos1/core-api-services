from django import forms
from .models import Vehiculo, Operario, Faena, Mantencion, RegistroIncidente

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['patente', 'tipo', 'marca', 'modelo', 'año', 'estado', 'horas_uso', 'capacidad_carga', 'fecha_adquisicion', 'observaciones']
        widgets = {
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'patente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABCD-12'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'año': forms.Select(choices=[(i, i) for i in range(1990, 2031)], attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'horas_uso': forms.Select(choices=[(i, i) for i in range(0, 20001, 500)], attrs={'class': 'form-select'}),
            'capacidad_carga': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_patente(self):
        patente = self.cleaned_data['patente'].upper()
        return patente

class OperarioForm(forms.ModelForm):
    class Meta:
        model = Operario
        fields = ['rut', 'nombre', 'rol', 'licencia', 'telefono', 'activo']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'licencia': forms.Select(choices=[
                ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'), 
                ('B', 'B'), ('D', 'D'), ('F', 'F')
            ], attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+569...'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if not Operario.validar_rut(rut):
            raise forms.ValidationError("El RUT ingresado no es válido.")
        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if telefono and not telefono.startswith('+569'):
            # Auto-format if user forgot +569 but entered 8 digits
            clean_num = ''.join(filter(str.isdigit, telefono))
            if len(clean_num) == 8:
                return f'+569{clean_num}'
            elif len(clean_num) == 9 and clean_num.startswith('9'):
                 return f'+56{clean_num}'
            elif not telefono.startswith('+'):
                return f'+569{telefono}'
        return telefono

class FaenaForm(forms.ModelForm):
    class Meta:
        model = Faena
        fields = ['nombre', 'tipo', 'estado', 'ubicacion', 'vehiculo', 'operario', 'fecha_inicio', 'fecha_termino', 'metros_cubicos', 'hectareas', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-select'}),
            'operario': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_termino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'metros_cubicos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'hectareas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
