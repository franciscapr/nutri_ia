from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Crea una contraseña segura',
            'class': 'form-control',
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repite la contraseña',
            'class': 'form-control',
        })
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingresa tu nombre'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingresa tus apellidos'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Ej: +56 9 1234 5678'
        self.fields['email'].widget.attrs['placeholder'] = 'correo@ejemplo.com'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
