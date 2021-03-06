from django.forms import ModelForm,Form
from .models import SocialAuth
from django import forms


class SocialAuthForm(forms.Form, ModelForm):
    name = forms.CharField(label="Full name", widget= forms.TextInput( attrs= {'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget= forms.EmailInput( attrs= {'class': 'form-control'}))
    mobile = forms.IntegerField(label="Phone number", required=False, widget= forms.TextInput( attrs= {'class': 'form-control'}))
    email_notifications = forms.BooleanField(label="Get notification about change in stream state and new user follows", required=False, initial=True,widget=forms.CheckboxInput(attrs={'class':"custom-control-input"}))

    class Meta:
        model = SocialAuth
        fields = ['mobile', 'email_notifications']