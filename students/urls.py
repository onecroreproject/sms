from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.student_create, name='student_add'),
    path('edit/<int:pk>/', views.student_update, name='student_edit'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    # New Import/Export Paths
    path('import/', views.import_students, name='import_students'),
    path('export/excel/', views.export_students_excel, name='export_excel'),
    path('export/pdf/', views.export_students_pdf, name='export_pdf'),
]
