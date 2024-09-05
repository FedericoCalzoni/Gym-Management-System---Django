from django import forms
from .import models

from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User 

class EnquiryForms(forms.ModelForm):
    class Meta:
        model = models.Enquiry

        fields = ('full_name','email','query')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(), required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']


class EditUserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class EditUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class TrainerLoginForm(forms.ModelForm):
    class Meta:
        model = models.Trainer
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

class EditTrainerProfileForm(UserChangeForm):
    class Meta:
        model = models.Trainer
        fields = ['full_name','mobile','address','details','img']


class EditTrainerPasswordForm(PasswordChangeForm):
    class Meta:
        model = models.Trainer
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }