from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm
import datetime
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def dashboard(request):
    queryset = Student.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(mobile__icontains=search_query) |
            Q(whatsapp__icontains=search_query) |
            Q(degree__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(passed_out_year__icontains=search_query)
        )

    # Filter functionality
    degree_filter = request.GET.get('degree')
    dept_filter = request.GET.get('department')
    year_filter = request.GET.get('year')

    if degree_filter:
        queryset = queryset.filter(degree__iexact=degree_filter)
    if dept_filter:
        queryset = queryset.filter(department__iexact=dept_filter)
    if year_filter:
        queryset = queryset.filter(passed_out_year=year_filter)

    # Summary Stats
    total_students = Student.objects.count()
    today = timezone.now().date()
    today_added = Student.objects.filter(created_at__date=today).count()

    # Pagination
    paginator = Paginator(queryset, 10) # 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get unique values for filters
    degrees = Student.objects.values_list('degree', flat=True).distinct()
    departments = Student.objects.values_list('department', flat=True).distinct()
    years = Student.objects.values_list('passed_out_year', flat=True).distinct().order_by('-passed_out_year')

    # Add student form for the modal
    form = StudentForm()

    context = {
        'students': page_obj,
        'total_students': total_students,
        'today_added': today_added,
        'degrees': degrees,
        'departments': departments,
        'years': years,
        'search_query': search_query,
        'selected_degree': degree_filter,
        'selected_dept': dept_filter,
        'selected_year': year_filter,
        'form': form,
    }
    return render(request, 'students/dashboard.html', context)

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student registered successfully!')
            return redirect('dashboard')
        else:
            # If form is invalid, re-render dashboard with errors and trigger modal
            return render_dashboard_with_errors(request, form)
    return redirect('dashboard')

def render_dashboard_with_errors(request, invalid_form):
    # This ensures the dashboard is rendered correctly but with the invalid form context
    queryset = Student.objects.all()
    # (Optional: Re-apply filters if needed, but usually creation is from clear state)
    
    total_students = Student.objects.count()
    today_added = Student.objects.filter(created_at__date=timezone.now().date()).count()
    
    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    degrees = Student.objects.values_list('degree', flat=True).distinct()
    departments = Student.objects.values_list('department', flat=True).distinct()
    years = Student.objects.values_list('passed_out_year', flat=True).distinct().order_by('-passed_out_year')

    context = {
        'students': page_obj,
        'total_students': total_students,
        'today_added': today_added,
        'degrees': degrees,
        'departments': departments,
        'years': years,
        'form': invalid_form,
        'show_modal': True,
    }
    return render(request, 'students/dashboard.html', context)

def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('dashboard')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Update Student', 'is_update': True})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student record deleted successfully!')
        return redirect('dashboard')
    return render(request, 'students/student_delete.html', {'student': student})

def import_students(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, 'Please upload a valid Excel file (.xlsx or .xls)')
            return redirect('dashboard')

        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            
            # Skip header row
            count = 0
            errors = []
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row[0]: continue # Skip empty rows
                
                name, mobile, whatsapp, degree, department, passed_out_year = row[:6]
                
                # Validation
                if Student.objects.filter(mobile=mobile).exists():
                    errors.append(f"Row {sheet.max_row}: Mobile {mobile} already exists.")
                    continue
                if Student.objects.filter(whatsapp=whatsapp).exists():
                    errors.append(f"Row {sheet.max_row}: WhatsApp {whatsapp} already exists.")
                    continue
                
                try:
                    Student.objects.create(
                        name=name,
                        mobile=str(mobile),
                        whatsapp=str(whatsapp),
                        degree=degree,
                        department=department,
                        passed_out_year=int(passed_out_year)
                    )
                    count += 1
                except Exception as e:
                    errors.append(f"Error in row with {name}: {str(e)}")

            if count > 0:
                messages.success(request, f'Successfully imported {count} students.')
            if errors:
                for err in errors[:5]: # Show first 5 errors
                    messages.warning(request, err)
                    
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
            
    return redirect('dashboard')

def export_students_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Students_{datetime.date.today()}.xlsx"'
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Students"
    
    # Header
    columns = ['Name', 'Mobile', 'WhatsApp', 'Degree', 'Department', 'Passed Out Year']
    ws.append(columns)
    
    # Data
    students = Student.objects.all()
    for student in students:
        ws.append([
            student.name,
            student.mobile,
            student.whatsapp,
            student.degree,
            student.department,
            student.passed_out_year
        ])
        
    wb.save(response)
    return response

def export_students_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Students_{datetime.date.today()}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []
    
    data = [['NAME', 'MOBILE', 'WHATSAPP', 'DEGREE', 'DEPT', 'YEAR']]
    students = Student.objects.all()
    for s in students:
        data.append([s.name, s.mobile, s.whatsapp, s.degree, s.department, str(s.passed_out_year)])
        
    table = Table(data, hAlign='LEFT', colWidths=[150, 100, 100, 100, 100, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.indigo),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    return response
