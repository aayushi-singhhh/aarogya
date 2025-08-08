# Hospital Portal System

## Description
A comprehensive hospital management portal system with three distinct user roles: Patient, Doctor, and Hospital Admin. Each role has specific functionalities and proper access control.

## Features

### Patient Portal
- **Profile Management**: Store personal information, medical history, allergies
- **Appointment Booking**: Book appointments with available doctors
- **Medical Records**: View diagnosis, treatments, prescriptions
- **Dashboard**: Overview of upcoming appointments and health status

### Doctor Portal
- **Schedule Management**: Set availability and manage time slots
- **Patient Management**: View assigned patients and their history
- **Appointment Handling**: Complete appointments with diagnosis and prescriptions
- **Medical Records**: Add diagnoses, treatments, and medications

### Hospital Admin Portal
- **User Management**: Add/remove doctors and patients
- **Assignment System**: Assign doctors to patients
- **Analytics**: Generate comprehensive reports and statistics
- **System Overview**: Monitor hospital operations and performance

## Project Structure
```
hospital_portal/
├── models/
│   ├── user.py              # Abstract base class for all users
│   ├── patient.py           # Patient class with medical records
│   ├── doctor.py            # Doctor class with scheduling
│   └── hospital_admin.py    # Admin class with management functions
├── portal_system.py         # Main system with CLI interface
└── README.md               # This file
```

## Installation and Setup

1. **Prerequisites**: Python 3.7 or higher

2. **No external dependencies required** - uses only Python standard library

3. **Run the system**:
   ```bash
   cd hospital_portal
   python portal_system.py
   ```

## Usage

### Initial Setup
1. Run the system and select "Initialize Demo Data" to create sample users
2. Use the provided demo credentials to login and explore features

### Demo Credentials
- **Admin**: admin@hospital.com / admin123
- **Doctor**: sarah@hospital.com / doc123  
- **Patient**: alice@email.com / pat123

### Core Functionalities

#### For Patients:
- Login and view personal dashboard
- Book appointments with available doctors
- View appointment history and medical records
- Update personal information and allergies

#### For Doctors:
- View assigned patients and appointment schedule
- Add diagnoses and medical records
- Manage appointment status (complete/cancel)
- Set availability and time slots

#### For Hospital Admins:
- Manage doctors and patients in the system
- Assign doctors to specific patients
- Generate various reports (patient demographics, doctor performance)
- View overall hospital statistics and performance

## Technical Implementation

### Object-Oriented Design
- **Inheritance**: All user types inherit from abstract `User` class
- **Encapsulation**: Private methods for internal operations
- **Polymorphism**: Role-specific implementations of abstract methods

### Security Features
- **Authentication**: Login system with password protection
- **Authorization**: Role-based access control
- **Account Security**: Login attempt limiting and account locking

### Data Management
- **In-Memory Storage**: All data stored in Python objects
- **Relationship Management**: Proper linking between patients, doctors, and appointments
- **Data Integrity**: Validation and error handling throughout

### Key Classes and Methods

#### Patient Class
```python
def book_appointment(self, doctor_id, date, reason) -> str
def view_appointments(self, status=None) -> List[Appointment]
def view_medical_reports() -> List[MedicalRecord]
def add_allergy(self, allergy: str)
```

#### Doctor Class
```python
def set_availability(self, date, start_time, end_time)
def add_diagnosis(self, patient_id, diagnosis, treatment) -> str
def manage_appointment(self, appointment_id, action, **kwargs) -> bool
def add_patient(self, patient_id: str)
```

#### HospitalAdmin Class
```python
def add_doctor(self, doctor: Doctor) -> bool
def assign_doctor_to_patient(self, patient_id, doctor_id) -> bool
def view_hospital_data() -> Dict
def generate_report(self, report_type, **kwargs) -> Dict
```

## System Capabilities

### Appointment Management
- Real-time scheduling system
- Conflict prevention and time slot management
- Status tracking (scheduled, completed, cancelled)
- Integration with doctor availability

### Medical Records
- Comprehensive patient history
- Diagnosis and treatment tracking
- Medication management with dosages
- Lab results and test data

### Reporting and Analytics
- Patient demographics and statistics
- Doctor performance metrics
- Appointment analytics and completion rates
- Department-wise analysis

### Role-Based Access Control
- **Patients**: Can only access their own data
- **Doctors**: Can access assigned patients and own schedule
- **Admins**: Have varying levels of system access based on admin level

## Future Enhancements
- Database integration for persistent storage
- Web interface using Flask/Django
- Email notifications for appointments
- Billing and payment integration
- Advanced reporting with charts and graphs
- Mobile app support
- Integration with external lab systems

## Error Handling
- Comprehensive input validation
- Graceful error recovery
- User-friendly error messages
- System stability under various conditions

This hospital portal system demonstrates professional software engineering practices including proper OOP design, security considerations, and user experience design suitable for real-world healthcare applications.
