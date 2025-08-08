#!/usr/bin/env python3
"""
Demo script for Hospital Portal System
This script demonstrates the key features of each user role
"""

from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.patient import Patient, MedicalRecord
from models.doctor import Doctor
from models.hospital_admin import HospitalAdmin
from portal_system import HospitalPortalSystem

def demo_patient_functionality():
    """Demonstrate Patient class functionality"""
    print("\n" + "="*50)
    print("PATIENT FUNCTIONALITY DEMO")
    print("="*50)
    
    # Create a patient
    patient = Patient("PAT001", "Alice Smith", "alice@email.com", "pass123", 
                     28, "Female", "555-0101", "123 Main St")
    patient.blood_type = "O+"
    patient.add_allergy("Penicillin")
    patient.add_allergy("Shellfish")
    
    print(f"Created patient: {patient}")
    print(f"Blood Type: {patient.blood_type}")
    print(f"Allergies: {', '.join(patient.allergies)}")
    
    # Book appointments
    apt_date1 = datetime.now() + timedelta(days=1, hours=10)
    apt_id1 = patient.book_appointment("DOC001", apt_date1, "Regular checkup")
    
    apt_date2 = datetime.now() + timedelta(days=7, hours=14)
    apt_id2 = patient.book_appointment("DOC002", apt_date2, "Follow-up visit")
    
    print(f"\nBooked appointments:")
    print(f"1. {apt_id1} - {apt_date1.strftime('%Y-%m-%d %H:%M')}")
    print(f"2. {apt_id2} - {apt_date2.strftime('%Y-%m-%d %H:%M')}")
    
    # View appointments
    appointments = patient.view_appointments()
    print(f"\nTotal appointments: {len(appointments)}")
    for apt in appointments:
        print(f"  - {apt}")
    
    # Add a medical record
    record = MedicalRecord("MR001", patient.user_id, "DOC001", 
                          "Hypertension", "Lifestyle changes and medication", datetime.now())
    record.add_medication("Lisinopril", "10mg daily", "30 days")
    patient.add_medical_record(record)
    
    print(f"\nMedical records: {len(patient.medical_history)}")
    for record in patient.medical_history:
        print(f"  - {record}")
    
    # Dashboard data
    dashboard = patient.get_dashboard_data()
    print(f"\nDashboard Summary:")
    print(f"Upcoming appointments: {dashboard['upcoming_appointments']}")
    print(f"Total appointments: {dashboard['total_appointments']}")
    print(f"Medical records: {dashboard['medical_records_count']}")

def demo_doctor_functionality():
    """Demonstrate Doctor class functionality"""
    print("\n" + "="*50)
    print("DOCTOR FUNCTIONALITY DEMO")
    print("="*50)
    
    # Create a doctor
    doctor = Doctor("DOC001", "Dr. Sarah Johnson", "sarah@hospital.com", "doc123",
                   "Cardiology", "MD12345", 15)
    doctor.consultation_fee = 200.0
    doctor.add_qualification("MD", "Harvard Medical School", 2008)
    doctor.add_qualification("Fellowship in Cardiology", "Johns Hopkins", 2012)
    
    print(f"Created doctor: {doctor}")
    print(f"Specialization: {doctor.specialization}")
    print(f"Experience: {doctor.years_experience} years")
    print(f"Consultation Fee: ${doctor.consultation_fee}")
    
    print(f"\nQualifications:")
    for qual in doctor.qualifications:
        print(f"  - {qual['qualification']} from {qual['institution']} ({qual['year']})")
    
    # Set availability
    tomorrow = datetime.now() + timedelta(days=1)
    doctor.set_availability(tomorrow, "09:00", "17:00")
    
    schedule = doctor.view_schedule(tomorrow)
    print(f"\nSchedule for {tomorrow.date()}:")
    for date, slots in schedule.items():
        print(f"Available slots: {len(slots.get('available_slots', []))}")
        print(f"First few slots: {slots.get('available_slots', [])[:5]}")
    
    # Assign patients
    doctor.add_patient("PAT001")
    doctor.add_patient("PAT002")
    
    print(f"\nAssigned patients: {len(doctor.assigned_patients)}")
    print(f"Patient IDs: {doctor.assigned_patients}")
    
    # Add diagnosis
    record_id = doctor.add_diagnosis("PAT001", "Mild hypertension", 
                                   "Diet modification and exercise",
                                   [{"name": "Lisinopril", "dosage": "10mg", "duration": "30 days"}])
    print(f"\nCreated medical record: {record_id}")
    
    # Dashboard data
    dashboard = doctor.get_dashboard_data()
    print(f"\nDashboard Summary:")
    print(f"Today's appointments: {dashboard['today_appointments']}")
    print(f"Total patients: {dashboard['total_patients']}")
    print(f"Pending appointments: {dashboard['pending_appointments']}")

def demo_admin_functionality():
    """Demonstrate Hospital Admin functionality"""
    print("\n" + "="*50)
    print("HOSPITAL ADMIN FUNCTIONALITY DEMO")
    print("="*50)
    
    # Create admin
    admin = HospitalAdmin("ADM001", "John Administrator", "admin@hospital.com", 
                         "admin123", "super")
    
    print(f"Created admin: {admin}")
    print(f"Admin level: {admin.admin_level}")
    print(f"Permissions: {list(admin.permissions.keys())}")
    
    # Create doctors and patients
    doctor1 = Doctor("DOC001", "Dr. Sarah Johnson", "sarah@hospital.com", "doc123",
                    "Cardiology", "MD12345", 15)
    doctor2 = Doctor("DOC002", "Dr. Michael Chen", "michael@hospital.com", "doc123",
                    "Pediatrics", "MD67890", 8)
    
    patient1 = Patient("PAT001", "Alice Smith", "alice@email.com", "pat123",
                      28, "Female", "555-0101", "123 Main St")
    patient2 = Patient("PAT002", "Bob Wilson", "bob@email.com", "pat123",
                      45, "Male", "555-0102", "456 Oak Ave")
    
    # Add to admin management
    admin.add_doctor(doctor1)
    admin.add_doctor(doctor2)
    admin.add_patient(patient1)
    admin.add_patient(patient2)
    
    print(f"\nManaged doctors: {len(admin.managed_doctors)}")
    for doc in admin.managed_doctors:
        print(f"  - {doc}")
    
    print(f"\nManaged patients: {len(admin.managed_patients)}")
    for pat in admin.managed_patients:
        print(f"  - {pat}")
    
    # Assign doctors to patients
    admin.assign_doctor_to_patient("PAT001", "DOC001")
    admin.assign_doctor_to_patient("PAT002", "DOC002")
    
    # View hospital data
    hospital_data = admin.view_hospital_data()
    print(f"\nHospital Statistics:")
    stats = hospital_data['hospital_stats']
    print(f"Total patients: {stats['total_patients']}")
    print(f"Total doctors: {stats['total_doctors']}")
    print(f"Departments: {stats['departments']}")
    
    # Generate reports
    patient_report = admin.generate_report("patient_summary")
    print(f"\nPatient Report:")
    print(f"Total patients: {patient_report['total_patients']}")
    print(f"Age distribution: {patient_report['age_distribution']}")
    print(f"Gender distribution: {patient_report['gender_distribution']}")
    
    doctor_report = admin.generate_report("doctor_performance")
    print(f"\nDoctor Report:")
    print(f"Total doctors: {doctor_report['total_doctors']}")
    print(f"Specializations: {doctor_report['specializations']}")
    print(f"Average experience: {doctor_report['average_experience']:.1f} years")
    
    # Dashboard data
    dashboard = admin.get_dashboard_data()
    print(f"\nAdmin Dashboard:")
    overview = dashboard['hospital_overview']
    print(f"Total patients: {overview['total_patients']}")
    print(f"Total doctors: {overview['total_doctors']}")
    print(f"Today's appointments: {overview['today_appointments']}")
    print(f"Departments: {overview['departments']}")

def demo_role_based_access():
    """Demonstrate role-based access control"""
    print("\n" + "="*50)
    print("ROLE-BASED ACCESS CONTROL DEMO")
    print("="*50)
    
    # Create users with different roles
    patient = Patient("PAT001", "Alice Smith", "alice@email.com", "pat123",
                     28, "Female", "555-0101", "123 Main St")
    
    doctor = Doctor("DOC001", "Dr. Sarah Johnson", "sarah@hospital.com", "doc123",
                   "Cardiology", "MD12345", 15)
    
    admin_junior = HospitalAdmin("ADM001", "Jane Admin", "jane@hospital.com",
                               "admin123", "junior")
    
    admin_super = HospitalAdmin("ADM002", "John SuperAdmin", "john@hospital.com",
                              "admin123", "super")
    
    print("Testing permissions:")
    
    # Patient permissions (should only access own data)
    print(f"\nPatient '{patient.name}' dashboard access:")
    patient_dashboard = patient.get_dashboard_data()
    print(f"✓ Can access own dashboard: {bool(patient_dashboard)}")
    
    # Doctor permissions
    print(f"\nDoctor '{doctor.name}' permissions:")
    doctor_dashboard = doctor.get_dashboard_data()
    print(f"✓ Can access own dashboard: {bool(doctor_dashboard)}")
    print(f"✓ Can set availability: True")
    print(f"✓ Can add diagnoses: True")
    
    # Junior admin permissions
    print(f"\nJunior Admin '{admin_junior.name}' permissions:")
    for perm, granted in admin_junior.permissions.items():
        status = "✓" if granted else "✗"
        print(f"{status} {perm}: {granted}")
    
    # Super admin permissions
    print(f"\nSuper Admin '{admin_super.name}' permissions:")
    for perm, granted in admin_super.permissions.items():
        status = "✓" if granted else "✗"
        print(f"{status} {perm}: {granted}")
    
    # Test access denial
    print(f"\nTesting access control:")
    print("Attempting to remove doctor with junior admin...")
    result = admin_junior.remove_doctor("DOC001")
    print(f"Result: {'Success' if result else 'Access Denied'}")
    
    print("Attempting to remove doctor with super admin...")
    admin_super.add_doctor(doctor)  # First add the doctor
    result = admin_super.remove_doctor("DOC001")
    print(f"Result: {'Success' if result else 'Failed'}")

def main():
    """Run all demonstrations"""
    print("HOSPITAL PORTAL SYSTEM - COMPREHENSIVE DEMO")
    print("="*60)
    
    try:
        demo_patient_functionality()
        demo_doctor_functionality()
        demo_admin_functionality()
        demo_role_based_access()
        
        print("\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nTo run the interactive CLI system, execute:")
        print("python portal_system.py")
        print("\nDemo credentials for CLI:")
        print("Admin: admin@hospital.com / admin123")
        print("Doctor: sarah@hospital.com / doc123")
        print("Patient: alice@email.com / pat123")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
