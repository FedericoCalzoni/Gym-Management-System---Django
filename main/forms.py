from django import forms
from .import models

from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User

class EnquiryForms(forms.ModelForm):
    class Meta:
        model = models.Enquiry

        fields = ('full_name','email','query')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(), required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
