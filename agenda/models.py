from django.db import models
from django.conf import settings    # Importamos el AUTH_USER_MODEL
from django.utils import timezone

# Modelo del nutricionista uno a uno - un usuario un nutricionista
class Nutritionist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    


class AppointmentSlot(models.Model):
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('nutritionist', 'date', 'time')  # Evita duplicados
    
    def __str__(self):
        status = "Ocupado" if self.is_booked else "Disponible"
        return f'{self.date} {self.time} - {status}'



class Appointment(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_appointments')
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Cita de {self.client.email} con {self.slot.nutritionist.user.email} - {self.slot.date} {self.slot.time}'
