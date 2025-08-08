from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from models.patient import Patient
from models.doctor import Doctor
from models.hospital_admin import HospitalAdmin
from models.user import User

class AuthenticationSystem:
    def __init__(self):
        self.users = {}  # email -> user object
        self.current_user = None
        self.login_attempts = {}  # email -> attempt count
        self.max_attempts = 3
    
    def register_user(self, user: User) -> bool:
        """Register a new user in the system"""
        if user.email in self.users:
            print(f"User with email {user.email} already exists")
            return False
        
        self.users[user.email] = user
        print(f"User {user.name} registered successfully as {user.role}")
        return True
    
    def login(self, email: str, password: str) -> Optional[User]:
        """Authenticate user and return user object if successful"""
        # Check if account is locked
        if email in self.login_attempts and self.login_attempts[email] >= self.max_attempts:
            print("Account locked due to too many failed attempts")
            return None
        
        if email not in self.users:
            print("User not found")
            self._record_failed_attempt(email)
            return None
        
        user = self.users[email]
        if user.password == password:
            self.current_user = user
            user.login()
            # Reset failed attempts on successful login
            if email in self.login_attempts:
                del self.login_attempts[email]
            print(f"Welcome, {user.name}!")
            return user
        else:
            print("Invalid password")
            self._record_failed_attempt(email)
            return None
    
    def _record_failed_attempt(self, email: str):
        """Record a failed login attempt"""
        if email not in self.login_attempts:
            self.login_attempts[email] = 0
        self.login_attempts[email] += 1
        
        remaining = self.max_attempts - self.login_attempts[email]
        if remaining > 0:
            print(f"Login failed. {remaining} attempts remaining.")
        else:
            print("Account locked due to too many failed attempts")
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            print(f"Goodbye, {self.current_user.name}!")
            self.current_user = None
        else:
            print("No user currently logged in")
    
    def get_current_user(self) -> Optional[User]:
        """Get currently logged in user"""
        return self.current_user
    
    def reset_password(self, email: str, new_password: str) -> bool:
        """Reset user password (simplified version)"""
        if email in self.users:
            self.users[email].password = new_password
            print("Password reset successfully")
            return True
        print("User not found")
        return False

class HospitalPortalSystem:
    def __init__(self):
        self.auth_system = AuthenticationSystem()
        self.appointment_counter = 0
        self.record_counter = 0
    
    def initialize_demo_data(self):
        """Initialize system with demo data"""
        # Create demo hospital admin
        admin = HospitalAdmin("ADM001", "John Administrator", "admin@hospital.com", "admin123", "super")
        
        # Create demo doctors
        doctor1 = Doctor("DOC001", "Dr. Sarah Johnson", "sarah@hospital.com", "doc123", 
                        "Cardiology", "MD12345", 15)
        doctor1.consultation_fee = 200.0
        doctor1.add_qualification("MD", "Harvard Medical School", 2008)
        doctor1.add_qualification("Fellowship in Cardiology", "Johns Hopkins", 2012)
        
        doctor2 = Doctor("DOC002", "Dr. Michael Chen", "michael@hospital.com", "doc123",
                        "Pediatrics", "MD67890", 8)
        doctor2.consultation_fee = 150.0
        doctor2.add_qualification("MD", "Stanford University", 2015)
        
        doctor3 = Doctor("DOC003", "Dr. Emily Rodriguez", "emily@hospital.com", "doc123",
                        "Neurology", "MD54321", 12)
        doctor3.consultation_fee = 250.0
        
        # Create demo patients
        patient1 = Patient("PAT001", "Alice Smith", "alice@email.com", "pat123", 
                          28, "Female", "555-0101", "123 Main St")
        patient1.blood_type = "O+"
        patient1.add_allergy("Penicillin")
        
        patient2 = Patient("PAT002", "Bob Wilson", "bob@email.com", "pat123",
                          45, "Male", "555-0102", "456 Oak Ave")
        patient2.blood_type = "A-"
        
        patient3 = Patient("PAT003", "Carol Davis", "carol@email.com", "pat123",
                          35, "Female", "555-0103", "789 Pine Rd")
        patient3.blood_type = "B+"
        patient3.add_allergy("Shellfish")
        patient3.add_allergy("Latex")
        
        # Register all users
        self.auth_system.register_user(admin)
        self.auth_system.register_user(doctor1)
        self.auth_system.register_user(doctor2)
        self.auth_system.register_user(doctor3)
        self.auth_system.register_user(patient1)
        self.auth_system.register_user(patient2)
        self.auth_system.register_user(patient3)
        
        # Add doctors and patients to admin management
        admin.add_doctor(doctor1)
        admin.add_doctor(doctor2)
        admin.add_doctor(doctor3)
        admin.add_patient(patient1)
        admin.add_patient(patient2)
        admin.add_patient(patient3)
        
        # Assign patients to doctors
        admin.assign_doctor_to_patient("PAT001", "DOC001")
        admin.assign_doctor_to_patient("PAT002", "DOC002")
        admin.assign_doctor_to_patient("PAT003", "DOC003")
        
        # Set doctor availability
        tomorrow = datetime.now() + timedelta(days=1)
        doctor1.set_availability(tomorrow, "09:00", "17:00")
        doctor2.set_availability(tomorrow, "10:00", "16:00")
        doctor3.set_availability(tomorrow, "08:00", "18:00")
        
        # Create some demo appointments
        apt_date1 = datetime.now() + timedelta(days=1, hours=10)
        apt_id1 = patient1.book_appointment("DOC001", apt_date1, "Chest pain")
        
        apt_date2 = datetime.now() + timedelta(days=2, hours=14)
        apt_id2 = patient2.book_appointment("DOC002", apt_date2, "Child vaccination")
        
        print("Demo data initialized successfully!")
        print("Demo login credentials:")
        print("Admin: admin@hospital.com / admin123")
        print("Doctor: sarah@hospital.com / doc123")
        print("Patient: alice@email.com / pat123")
    
    def run_cli(self):
        """Run the command-line interface"""
        print("="*50)
        print("HOSPITAL PORTAL SYSTEM")
        print("="*50)
        
        while True:
            if not self.auth_system.current_user:
                self._show_login_menu()
            else:
                self._show_user_menu()
    
    def _show_login_menu(self):
        """Show login/registration menu"""
        print("\n" + "="*30)
        print("LOGIN MENU")
        print("="*30)
        print("1. Login")
        print("2. Initialize Demo Data")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            self._handle_login()
        elif choice == "2":
            self.initialize_demo_data()
        elif choice == "3":
            print("Thank you for using Hospital Portal System!")
            exit()
        else:
            print("Invalid choice. Please try again.")
    
    def _handle_login(self):
        """Handle user login"""
        print("\n" + "-"*20)
        print("LOGIN")
        print("-"*20)
        
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        
        user = self.auth_system.login(email, password)
        if user:
            self._show_dashboard(user)
    
    def _show_user_menu(self):
        """Show menu based on user role"""
        user = self.auth_system.current_user
        
        print(f"\n" + "="*50)
        print(f"WELCOME, {user.name.upper()} ({user.role.upper()})")
        print("="*50)
        
        if isinstance(user, Patient):
            self._show_patient_menu()
        elif isinstance(user, Doctor):
            self._show_doctor_menu()
        elif isinstance(user, HospitalAdmin):
            self._show_admin_menu()
    
    def _show_dashboard(self, user: User):
        """Show role-specific dashboard"""
        dashboard_data = user.get_dashboard_data()
        
        print(f"\n" + "="*40)
        print(f"{user.role.upper()} DASHBOARD")
        print("="*40)
        
        if isinstance(user, Patient):
            info = dashboard_data["user_info"]
            print(f"Name: {info['name']}")
            print(f"Age: {info['age']}")
            print(f"Blood Type: {info.get('blood_type', 'Not specified')}")
            print(f"Allergies: {', '.join(info['allergies']) if info['allergies'] else 'None'}")
            print(f"\nUpcoming Appointments: {dashboard_data['upcoming_appointments']}")
            print(f"Total Appointments: {dashboard_data['total_appointments']}")
            print(f"Medical Records: {dashboard_data['medical_records_count']}")
            
        elif isinstance(user, Doctor):
            info = dashboard_data["user_info"]
            print(f"Name: {info['name']}")
            print(f"Specialization: {info['specialization']}")
            print(f"Experience: {info['experience']}")
            print(f"Consultation Fee: ${dashboard_data['consultation_fee']}")
            print(f"\nToday's Appointments: {dashboard_data['today_appointments']}")
            print(f"Total Patients: {dashboard_data['total_patients']}")
            print(f"Pending Appointments: {dashboard_data['pending_appointments']}")
            
        elif isinstance(user, HospitalAdmin):
            info = dashboard_data["user_info"]
            overview = dashboard_data["hospital_overview"]
            print(f"Name: {info['name']}")
            print(f"Admin Level: {info['admin_level']}")
            print(f"\nHospital Overview:")
            print(f"Total Patients: {overview['total_patients']}")
            print(f"Total Doctors: {overview['total_doctors']}")
            print(f"Today's Appointments: {overview['today_appointments']}")
            print(f"Departments: {overview['departments']}")
    
    def _show_patient_menu(self):
        """Show patient-specific menu"""
        print("\nPATIENT MENU:")
        print("1. View Dashboard")
        print("2. Book Appointment")
        print("3. View Appointments")
        print("4. View Medical Records")
        print("5. Update Personal Info")
        print("6. Logout")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            self._show_dashboard(self.auth_system.current_user)
        elif choice == "2":
            self._book_appointment()
        elif choice == "3":
            self._view_patient_appointments()
        elif choice == "4":
            self._view_medical_records()
        elif choice == "5":
            self._update_patient_info()
        elif choice == "6":
            self.auth_system.logout()
        else:
            print("Invalid choice. Please try again.")
    
    def _show_doctor_menu(self):
        """Show doctor-specific menu"""
        print("\nDOCTOR MENU:")
        print("1. View Dashboard")
        print("2. View Schedule")
        print("3. View Appointments")
        print("4. Add Diagnosis")
        print("5. Manage Appointments")
        print("6. View Assigned Patients")
        print("7. Set Availability")
        print("8. Logout")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            self._show_dashboard(self.auth_system.current_user)
        elif choice == "2":
            self._view_doctor_schedule()
        elif choice == "3":
            self._view_doctor_appointments()
        elif choice == "4":
            self._add_diagnosis()
        elif choice == "5":
            self._manage_appointments()
        elif choice == "6":
            self._view_assigned_patients()
        elif choice == "7":
            self._set_availability()
        elif choice == "8":
            self.auth_system.logout()
        else:
            print("Invalid choice. Please try again.")
    
    def _show_admin_menu(self):
        """Show admin-specific menu"""
        print("\nADMIN MENU:")
        print("1. View Dashboard")
        print("2. View Hospital Data")
        print("3. Manage Doctors")
        print("4. Manage Patients")
        print("5. Assign Doctor to Patient")
        print("6. Generate Reports")
        print("7. View All Appointments")
        print("8. Logout")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            self._show_dashboard(self.auth_system.current_user)
        elif choice == "2":
            self._view_hospital_data()
        elif choice == "3":
            self._manage_doctors()
        elif choice == "4":
            self._manage_patients()
        elif choice == "5":
            self._assign_doctor_to_patient()
        elif choice == "6":
            self._generate_reports()
        elif choice == "7":
            self._view_all_appointments()
        elif choice == "8":
            self.auth_system.logout()
        else:
            print("Invalid choice. Please try again.")
    
    def _book_appointment(self):
        """Handle appointment booking"""
        patient = self.auth_system.current_user
        
        print("\n" + "-"*30)
        print("BOOK APPOINTMENT")
        print("-"*30)
        
        # Show available doctors
        admin = self._get_admin()
        if not admin:
            print("System error: No admin found")
            return
        
        print("Available Doctors:")
        for i, doctor in enumerate(admin.managed_doctors, 1):
            print(f"{i}. Dr. {doctor.name} - {doctor.specialization} (Fee: ${doctor.consultation_fee})")
        
        try:
            doc_choice = int(input("\nSelect doctor (number): ")) - 1
            if 0 <= doc_choice < len(admin.managed_doctors):
                selected_doctor = admin.managed_doctors[doc_choice]
                
                print(f"\nBooking with Dr. {selected_doctor.name}")
                reason = input("Reason for visit: ").strip()
                
                # For demo, book for tomorrow at 10 AM
                apt_date = datetime.now() + timedelta(days=1, hours=10)
                apt_id = patient.book_appointment(selected_doctor.user_id, apt_date, reason)
                
                print(f"Appointment booked successfully!")
                print(f"Appointment ID: {apt_id}")
                print(f"Date: {apt_date.strftime('%Y-%m-%d %H:%M')}")
                print(f"Doctor: Dr. {selected_doctor.name}")
                
            else:
                print("Invalid doctor selection")
        except ValueError:
            print("Please enter a valid number")
    
    def _view_patient_appointments(self):
        """View patient's appointments"""
        patient = self.auth_system.current_user
        
        print("\n" + "-"*30)
        print("YOUR APPOINTMENTS")
        print("-"*30)
        
        appointments = patient.view_appointments()
        if not appointments:
            print("No appointments found")
            return
        
        for apt in appointments:
            print(f"ID: {apt.appointment_id}")
            print(f"Date: {apt.date.strftime('%Y-%m-%d %H:%M')}")
            print(f"Reason: {apt.reason}")
            print(f"Status: {apt.status}")
            if apt.diagnosis:
                print(f"Diagnosis: {apt.diagnosis}")
            print("-" * 20)
    
    def _view_medical_records(self):
        """View patient's medical records"""
        patient = self.auth_system.current_user
        
        print("\n" + "-"*30)
        print("MEDICAL RECORDS")
        print("-"*30)
        
        records = patient.view_medical_reports()
        if not records:
            print("No medical records found")
            return
        
        for record in records:
            print(f"Record ID: {record.record_id}")
            print(f"Date: {record.date.strftime('%Y-%m-%d')}")
            print(f"Diagnosis: {record.diagnosis}")
            print(f"Treatment: {record.treatment}")
            if record.medications:
                print("Medications:")
                for med in record.medications:
                    print(f"  - {med['medication']} ({med['dosage']}) for {med['duration']}")
            print("-" * 30)
    
    def _update_patient_info(self):
        """Update patient information"""
        patient = self.auth_system.current_user
        
        print("\n" + "-"*30)
        print("UPDATE PERSONAL INFO")
        print("-"*30)
        
        print("Current Information:")
        print(f"Phone: {patient.phone}")
        print(f"Address: {patient.address}")
        print(f"Blood Type: {patient.blood_type or 'Not set'}")
        
        new_phone = input(f"\nNew phone ({patient.phone}): ").strip()
        new_address = input(f"New address ({patient.address}): ").strip()
        new_blood_type = input(f"Blood type ({patient.blood_type or 'Not set'}): ").strip()
        
        updates = {}
        if new_phone:
            updates['phone'] = new_phone
        if new_address:
            updates['address'] = new_address
        if new_blood_type:
            updates['blood_type'] = new_blood_type
        
        if updates:
            patient.update_personal_info(**updates)
            print("Information updated successfully!")
        else:
            print("No changes made")
    
    def _get_admin(self) -> Optional[HospitalAdmin]:
        """Get the first admin from the system"""
        for user in self.auth_system.users.values():
            if isinstance(user, HospitalAdmin):
                return user
        return None
    
    # Additional methods for doctor and admin functionality would go here...
    # (Truncated for brevity, but can be expanded with full implementations)
    
    def _view_doctor_schedule(self):
        """View doctor's schedule"""
        doctor = self.auth_system.current_user
        tomorrow = datetime.now() + timedelta(days=1)
        schedule = doctor.view_schedule(tomorrow)
        
        print("\n" + "-"*30)
        print("YOUR SCHEDULE")
        print("-"*30)
        
        for date, slots in schedule.items():
            print(f"Date: {date}")
            print(f"Available slots: {slots.get('available_slots', [])}")
            print(f"Booked slots: {slots.get('booked_slots', [])}")
    
    def _view_hospital_data(self):
        """View hospital data (admin only)"""
        admin = self.auth_system.current_user
        data = admin.view_hospital_data()
        
        print("\n" + "-"*30)
        print("HOSPITAL DATA")
        print("-"*30)
        
        stats = data.get('hospital_stats', {})
        print(f"Total Patients: {stats.get('total_patients', 0)}")
        print(f"Total Doctors: {stats.get('total_doctors', 0)}")
        print(f"Total Appointments: {stats.get('total_appointments', 0)}")
        print(f"Completed Appointments: {stats.get('completed_appointments', 0)}")
        
        print("\nDepartments:")
        departments = stats.get('departments', {})
        for dept, count in departments.items():
            print(f"  {dept}: {count} doctors")

if __name__ == "__main__":
    portal = HospitalPortalSystem()
    portal.run_cli()
