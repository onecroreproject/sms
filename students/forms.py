from django import forms
from .models import Student
import datetime
import re

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'mobile', 'whatsapp', 'degree', 'department', 'passed_out_year', 'college_name', 'form_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter WhatsApp Number'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Degree (e.g. B.E)'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department (e.g. CSE)'}),
            'passed_out_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Passing Year'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter College Name'}),
            'form_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Form Name'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or email.strip() == "" or email == "None":
            return None
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile or mobile.strip() == "" or mobile == "None":
            return None
        if not re.match(r'^\+?1?\d{9,15}$', mobile):
            raise forms.ValidationError("Enter a valid phone number (9-15 digits).")
        return mobile

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if not whatsapp or whatsapp.strip() == "" or whatsapp == "None":
            return None
        if not re.match(r'^\+?1?\d{9,15}$', whatsapp):
            raise forms.ValidationError("Enter a valid WhatsApp number (9-15 digits).")
        return whatsapp

    def clean_passed_out_year(self):
        year = self.cleaned_data.get('passed_out_year')
        if not year or str(year) == "None":
            return None
        try:
            year_int = int(year)
        except (ValueError, TypeError):
            return None
            
        current_year = datetime.date.today().year
        if year_int < 1950 or year_int > current_year + 10:
            raise forms.ValidationError(f"Please enter a valid year between 1950 and {current_year + 10}.")
        return year_int

    def clean_degree(self):
        val = self.cleaned_data.get('degree')
        if not val or val == "None": return None
        return val

    def clean_department(self):
        val = self.cleaned_data.get('department')
        if not val or val == "None": return None
        return val

    def clean_name(self):
        val = self.cleaned_data.get('name')
        if not val or val == "None": return None
        return val

    def clean_form_name(self):
        form_name = self.cleaned_data.get('form_name')
        if not form_name or form_name.strip() == "":
            return None
        return form_name
