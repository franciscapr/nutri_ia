from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import AppointmentSlot, Appointment
from .forms import AppointmentForm  # crearemos este formulario más adelante
from datetime import date
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings


def agenda_citas(request):
    slots = AppointmentSlot.objects.filter(date__gte=date.today()).values('date', 'time', 'is_booked')
    return render(request, 'agenda/agenda_citas.html', {
        'slots': list(slots)  # Esto lo hace serializable
    })

@login_required
def reservar_cita(request, fecha, hora):
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()

    # Filtrar el slot correspondiente a la fecha y hora seleccionadas
    slot = AppointmentSlot.objects.filter(date=fecha_obj, time=hora, is_booked=False).first()

    if not slot:
        # Si no hay un slot disponible
        return HttpResponse("El slot ya está reservado o no está disponible.")

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.slot = slot  # Asignamos el slot seleccionado
            appointment.client = request.user  # Asignamos el usuario autenticado como el cliente

            # Marcar el slot como reservado
            slot.is_booked = True
            slot.save()

            appointment.save()
            return redirect('confirmacion_cita', cita_id=appointment.id)
    else:
        form = AppointmentForm(initial={'slot': slot})

    return render(request, 'agenda/reservar_cita.html', {
        'fecha': fecha_obj,
        'hora': hora,
        'form': form,
        'slot': slot
    })

def confirmacion_cita(request, cita_id):
    # Obtener la cita usando el ID
    cita = Appointment.objects.get(id=cita_id)

    return render(request, 'agenda/confirmacion_cita.html', {'cita': cita})



