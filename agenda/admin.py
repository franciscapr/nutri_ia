from django.contrib import admin
from .models import Nutritionist, AppointmentSlot, Appointment, Specialty

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Nutritionist)
class NutritionistAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty')
    search_fields = ('user__email', 'specialty')

@admin.register(AppointmentSlot)
class AppointmentSlotAdmin(admin.ModelAdmin):
    list_display = ('nutritionist', 'date', 'time', 'is_booked')
    list_filter = ('nutritionist', 'date', 'is_booked')
    search_fields = ('nutritionist__user__email',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'slot', 'get_nutritionist', 'slot_date', 'slot_time')
    search_fields = ('client__email', 'slot__nutritionist__user__email')
    list_filter = ('slot__date',)

    def get_nutritionist(self, obj):
        return obj.slot.nutritionist
    get_nutritionist.short_description = 'Nutricionista'

    def slot_date(self, obj):
        return obj.slot.date
    def slot_time(self, obj):
        return obj.slot.time

