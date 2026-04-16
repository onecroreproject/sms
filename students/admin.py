from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'degree', 'department', 'passed_out_year')
    search_fields = ('name', 'mobile', 'whatsapp', 'degree', 'department')
    list_filter = ('degree', 'department', 'passed_out_year')
