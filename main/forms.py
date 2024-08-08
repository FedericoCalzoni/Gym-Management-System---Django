from django import forms
from .import models


class EnquiryForms(forms.ModelForm):
    class Meta:
        model = models.Enquiry

        fields = ('full_name','query','email')