import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_project.settings')
django.setup()

from students.models import Student

def seed_duplicates():
    # Sample data with duplicates
    students_data = [
        {
            'name': 'Shreya Bansal',
            'email': 'shreya.bansal@example.com',
            'mobile': '9876566168',
            'whatsapp': '9123411763',
            'degree': 'B.Tech',
            'department': 'Civil Engineering',
            'passed_out_year': 2020
        },
        {
            'name': 'Shreya Duplicate',
            'email': 'shreya.bansal@example.com', # Duplicate Email
            'mobile': '9876566168', # Duplicate Mobile
            'whatsapp': '9123411763',
            'degree': 'B.Tech',
            'department': 'Civil Engineering',
            'passed_out_year': 2020
        },
        {
            'name': 'Pranav Deshmukh',
            'email': 'pranav.deshmukh@example.com',
            'mobile': '9876574574',
            'whatsapp': '9123440489',
            'degree': 'B.Tech',
            'department': 'Civil Engineering',
            'passed_out_year': 2021
        },
        {
            'name': 'Kavita Iyer',
            'email': 'kavita.iyer@example.com',
            'mobile': '9876517902',
            'whatsapp': '9123439721',
            'degree': 'B.Com',
            'department': 'Electrical Engineering',
            'passed_out_year': 2022
        },
        {
            'name': 'Kavita Duplicate',
            'email': 'kavita.iyer@example.com', # Duplicate Email
            'mobile': '0000000000',
            'whatsapp': '0000000000',
            'degree': 'B.Com',
            'department': 'Electrical Engineering',
            'passed_out_year': 2022
        },
        {
            'name': 'Aditya Malhotra',
            'email': 'aditya.malhotra@example.com',
            'mobile': '9876578154',
            'whatsapp': '9123439995',
            'degree': 'B.Sc',
            'department': 'Electronics',
            'passed_out_year': 2020
        }
    ]

    for data in students_data:
        Student.objects.create(**data)
    
    print(f"Successfully added {len(students_data)} records, including duplicates.")

if __name__ == "__main__":
    seed_duplicates()
