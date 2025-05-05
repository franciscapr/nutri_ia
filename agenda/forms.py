from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    note = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Motivo de la cita'}),
        label="Nota para el nutricionista", 
        required=False
    )

    class Meta:
        model = Appointment
        fields = ['note']
