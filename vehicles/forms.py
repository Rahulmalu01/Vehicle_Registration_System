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
        fields = '__all__'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.endswith('.jpg'):
                raise forms.ValidationError("Only .jpg files are allowed.")
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image size should be less than 10MB.")
        return image

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
