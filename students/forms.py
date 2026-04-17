from django import forms
from .models import Student
import datetime
import re

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'mobile', 'whatsapp', 'degree', 'department', 'passed_out_year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp Number'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Degree (e.g. B.E)'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department (e.g. CSE)'}),
            'passed_out_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Passing Year'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\+?1?\d{9,15}$', mobile):
            raise forms.ValidationError("Enter a valid phone number (9-15 digits).")
        return mobile

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if not re.match(r'^\+?1?\d{9,15}$', whatsapp):
            raise forms.ValidationError("Enter a valid WhatsApp number (9-15 digits).")
        return whatsapp

    def clean_passed_out_year(self):
        year = self.cleaned_data.get('passed_out_year')
        current_year = datetime.date.today().year
        # Allow passing year up to 5 years in future (for current students) or anything in past
        if year < 1950 or year > current_year + 10:
            raise forms.ValidationError(f"Please enter a valid year between 1950 and {current_year + 10}.")
        return year
