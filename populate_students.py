import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_project.settings')
django.setup()

from students.models import Student

def populate(n=20):
    names = [
        "Arun Kumar", "Bala Murali", "Chitra Devi", "Deepak Raj", "Eswari S",
        "Farooq Ahmed", "Ganesh Ram", "Harini V", "Indira K", "Jeeva R",
        "Karthick M", "Laxmi Priya", "Mani Kandan", "Naveen S", "Oviya R",
        "Prakash J", "Qadir Khan", "Ramya S", "Suresh B", "Tharun K"
    ]
    
    degrees = ["B.E", "B.Tech", "B.Sc", "B.CA", "B.Com"]
    departments = ["CSE", "ECE", "EEE", "IT", "MECH", "CIVIL", "BioTech"]
    years = [2020, 2021, 2022, 2023, 2024, 2025]

    print(f"Adding {n} sample records...")
    
    for i in range(n):
        name = names[i % len(names)]
        if i >= len(names):
            name += f" {i}"
            
        mobile = f"9876543{i:03d}"
        whatsapp = f"9123456{i:03d}"
        degree = random.choice(degrees)
        department = random.choice(departments)
        passed_year = random.choice(years)
        
        # Check if mobile exists to avoid unique constraint error
        if not Student.objects.filter(mobile=mobile).exists():
            Student.objects.create(
                name=name,
                mobile=mobile,
                whatsapp=whatsapp,
                degree=degree,
                department=department,
                passed_out_year=passed_year
            )
            print(f"Added: {name}")
        else:
            print(f"Skipping {name} (Duplicate)")

    print("Populate finished successfully!")

if __name__ == '__main__':
    populate(20)
