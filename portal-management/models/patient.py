from datetime import datetime
from typing import List, Dict, Optional
from .user import User

class Appointment:
    def __init__(self, appointment_id: str, patient_id: str, doctor_id: str, 
                 date: datetime, reason: str, status: str = "scheduled"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.reason = reason
        self.status = status  # scheduled, completed, cancelled
        self.diagnosis = None
        self.prescription = None
        self.notes = None
    
    def complete_appointment(self, diagnosis: str, prescription: str = None, notes: str = None):
        """Mark appointment as completed with medical details"""
        self.status = "completed"
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.notes = notes
    
    def cancel_appointment(self):
        """Cancel the appointment"""
        self.status = "cancelled"
    
    def __str__(self):
        return f"Appointment {self.appointment_id}: {self.date.strftime('%Y-%m-%d %H:%M')} - {self.status}"

class MedicalRecord:
    def __init__(self, record_id: str, patient_id: str, doctor_id: str, 
                 diagnosis: str, treatment: str, date: datetime):
        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.date = date
        self.medications = []
        self.lab_results = {}
    
    def add_medication(self, medication: str, dosage: str, duration: str):
        """Add medication to the record"""
        self.medications.append({
            'medication': medication,
            'dosage': dosage,
            'duration': duration,
            'prescribed_date': datetime.now()
        })
    
    def add_lab_result(self, test_name: str, result: str, normal_range: str = None):
        """Add lab test result"""
        self.lab_results[test_name] = {
            'result': result,
            'normal_range': normal_range,
            'test_date': datetime.now()
        }
    
    def __str__(self):
        return f"Medical Record {self.record_id}: {self.diagnosis} on {self.date.strftime('%Y-%m-%d')}"

class Patient(User):
    def __init__(self, user_id: str, name: str, email: str, password: str, 
                 age: int, gender: str, phone: str, address: str):
        super().__init__(user_id, name, email, password, "Patient")
        self.age = age
        self.gender = gender
        self.phone = phone
        self.address = address
        self.medical_history: List[MedicalRecord] = []
        self.appointments: List[Appointment] = []
        self.emergency_contact = None
        self.insurance_info = None
        self.blood_type = None
        self.allergies = []
    
    def book_appointment(self, doctor_id: str, date: datetime, reason: str) -> str:
        """Book an appointment with a doctor"""
        appointment_id = f"APT_{len(self.appointments) + 1:04d}_{self.user_id}"
        appointment = Appointment(appointment_id, self.user_id, doctor_id, date, reason)
        self.appointments.append(appointment)
        return appointment_id
    
    def view_appointments(self, status: str = None) -> List[Appointment]:
        """View appointments, optionally filtered by status"""
        if status:
            return [apt for apt in self.appointments if apt.status == status]
        return self.appointments
    
    def view_medical_reports(self) -> List[MedicalRecord]:
        """View all medical records"""
        return self.medical_history
    
    def add_medical_record(self, record: MedicalRecord):
        """Add a medical record to patient's history"""
        self.medical_history.append(record)
    
    def update_personal_info(self, **kwargs):
        """Update personal information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def add_allergy(self, allergy: str):
        """Add an allergy to patient's record"""
        if allergy not in self.allergies:
            self.allergies.append(allergy)
    
    def get_dashboard_data(self) -> Dict:
        """Return patient dashboard data"""
        upcoming_appointments = [apt for apt in self.appointments 
                               if apt.status == "scheduled" and apt.date > datetime.now()]
        recent_records = sorted(self.medical_history, key=lambda x: x.date, reverse=True)[:5]
        
        return {
            "user_info": {
                "name": self.name,
                "age": self.age,
                "blood_type": self.blood_type,
                "allergies": self.allergies
            },
            "upcoming_appointments": len(upcoming_appointments),
            "total_appointments": len(self.appointments),
            "medical_records_count": len(self.medical_history),
            "recent_records": [str(record) for record in recent_records],
            "next_appointment": upcoming_appointments[0] if upcoming_appointments else None
        }
    
    def __str__(self):
        return f"Patient: {self.name} (Age: {self.age}, ID: {self.user_id})"
