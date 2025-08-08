#!/usr/bin/env python3
"""
Quick start example for Hospital Portal System
This shows how to use the system programmatically
"""

from datetime import datetime, timedelta
from models.patient import Patient
from models.doctor import Doctor
from models.hospital_admin import HospitalAdmin
from portal_system import HospitalPortalSystem

def quick_example():
    """Quick example of system usage"""
    print("HOSPITAL PORTAL SYSTEM - QUICK START EXAMPLE")
    print("=" * 50)
    
    # Create and initialize the portal system
    portal = HospitalPortalSystem()
    
    # Create users
    admin = HospitalAdmin("ADM001", "Hospital Admin", "admin@test.com", "admin123", "super")
    doctor = Doctor("DOC001", "Dr. Smith", "doctor@test.com", "doc123", "General Medicine", "MD123", 10)
    patient = Patient("PAT001", "John Doe", "patient@test.com", "pat123", 30, "Male", "555-1234", "123 Main St")
    
    # Register users in the system
    portal.auth_system.register_user(admin)
    portal.auth_system.register_user(doctor)
    portal.auth_system.register_user(patient)
    
    # Admin adds doctor and patient to management
    admin.add_doctor(doctor)
    admin.add_patient(patient)
    
    # Assign doctor to patient
    admin.assign_doctor_to_patient(patient.user_id, doctor.user_id)
    
    # Patient books appointment
    appointment_date = datetime.now() + timedelta(days=1, hours=10)
    apt_id = patient.book_appointment(doctor.user_id, appointment_date, "Regular checkup")
    
    print(f"✓ Created appointment: {apt_id}")
    print(f"✓ Date: {appointment_date.strftime('%Y-%m-%d %H:%M')}")
    
    # Doctor adds diagnosis
    record_id = doctor.add_diagnosis(patient.user_id, "Healthy", "Continue regular exercise")
    print(f"✓ Created medical record: {record_id}")
    
    # View dashboards
    print("\n--- PATIENT DASHBOARD ---")
    patient_data = patient.get_dashboard_data()
    print(f"Upcoming appointments: {patient_data['upcoming_appointments']}")
    
    print("\n--- DOCTOR DASHBOARD ---")
    doctor_data = doctor.get_dashboard_data()
    print(f"Total patients: {doctor_data['total_patients']}")
    
    print("\n--- ADMIN DASHBOARD ---")
    admin_data = admin.get_dashboard_data()
    print(f"Total patients: {admin_data['hospital_overview']['total_patients']}")
    print(f"Total doctors: {admin_data['hospital_overview']['total_doctors']}")
    
    print("\n✓ System working correctly!")

if __name__ == "__main__":
    quick_example()
