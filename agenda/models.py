from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError


def validate_weekday_and_future(value):
    if value < date.today():
        raise ValidationError("No puedes seleccionar una fecha pasada.")
    if value.weekday() >= 5:  # 5: sábado, 6: domingo
        raise ValidationError("Selecciona un día hábil (lunes a viernes).")

class Specialty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Nutritionist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class AppointmentSlot(models.Model):
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE)
    date = models.DateField(validators=[validate_weekday_and_future])
    
    TIME_CHOICES = [
        ("07:00", "07:00 - 08:00"),
        ("08:00", "08:00 - 09:00"),
        ("09:00", "09:00 - 10:00"),
        # Agrega más si quieres
    ]
    time = models.CharField(max_length=5, choices=TIME_CHOICES)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('nutritionist', 'date', 'time')

    def __str__(self):
        status = "Ocupado" if self.is_booked else "Disponible"
        return f'{self.date} {self.get_time_display()} - {status}'

class Appointment(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.client} con {self.slot.nutritionist} - {self.slot.date} {self.slot.time}'
