from django import forms
from .models import AppointmentSlot, Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['slot', 'notes']

    slot = forms.ModelChoiceField(queryset=AppointmentSlot.objects.filter(is_booked=False), empty_label="Seleccionar hora")
