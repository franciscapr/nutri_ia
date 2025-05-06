from django.urls import path
from . import views

urlpatterns = [
    # Ruta para ver la agenda (calendario)
    path('', views.agenda_citas, name='agenda_citas'),  # si accedes a /agenda/
    path('reservar/<str:fecha>/<str:hora>/', views.reservar_cita, name='reservar_cita'),
    path('confirmacion_cita/<int:cita_id>/', views.confirmacion_cita, name='confirmacion_cita'),
]
