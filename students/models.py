from django.db import models
from django.utils import timezone

class Student(models.Model):
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15, unique=True)
    whatsapp = models.CharField(max_length=15, unique=True)
    degree = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    passed_out_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
