from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import AppointmentSlot, Appointment
from .forms import AppointmentForm  # crearemos este formulario más adelante
from datetime import date
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings


# Calendar --> Visualizamos el calendario con los dias y la shoras disponibles.
def agenda_citas(request):
    slots = AppointmentSlot.objects.select_related('nutritionist__user').filter(date__gte=date.today(), is_booked=False)

    slot_data = []
    for slot in slots:
        slot_data.append({
            'date': slot.date.isoformat(),
            'time': slot.time,
            'is_booked': slot.is_booked,
            'nutritionist': f'{slot.nutritionist.user.first_name} {slot.nutritionist.user.last_name}',
            'url': f'/agenda/reservar/{slot.date}/{slot.time}/'
        })

    return render(request, 'agenda/agenda_citas.html', {
        'slots': slot_data
    })



@login_required
def reservar_cita(request, fecha, hora):
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()    # Obtenemos la fecha y hora --> convertimos a date
    slot = AppointmentSlot.objects.filter(date=fecha_obj, time=hora, is_booked=False).first()    # Buscamos el cita disponible

    # Si no se encuentra la cita, enviamos un mensaje
    if not slot:
        return HttpResponse("El slot ya está reservado o no está disponible.")

    # Procesamos el formulario si es de tipo post
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():    # Si el formulario es valido
            appointment = form.save(commit=False)
            appointment.slot = slot
            appointment.client = request.user

            # Marcar el slot como reservado
            slot.is_booked = True
            slot.save()
            appointment.save()

            return redirect('confirmacion_cita', cita_id=appointment.id)

    else:
        form = AppointmentForm(initial={'slot': slot})

    return render(request, 'agenda/confirmacion_cita.html', {
        'fecha': fecha_obj,
        'hora': hora,
        'form': form,
        'slot': slot
    })



@login_required
def confirmacion_cita(request, cita_id):
    cita = get_object_or_404(Appointment, id=cita_id, client=request.user)
    precio = cita.slot.nutritionist.price  # ← Asegúrate que esto no sea None

    return render(request, 'agenda/confirmacion_cita.html', {
        'cita': cita,
        'slot': cita.slot,
        'price': precio
    })
