from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehicle
from .models import Booking

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'vehicle_type', 'available', 'fare', 'model_name', 'make']
        widgets = {
            'fare': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter fare'}),
            'model_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter model name'}),
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter make'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []