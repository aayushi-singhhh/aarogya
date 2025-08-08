from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .user import User
from .patient import Appointment, MedicalRecord

class Schedule:
    def __init__(self):
        self.time_slots = {}  # date -> list of time slots
        self.booked_slots = {}  # date -> list of booked times
    
    def add_availability(self, date: datetime, start_time: str, end_time: str, slot_duration: int = 30):
        """Add available time slots for a specific date"""
        date_key = date.date()
        if date_key not in self.time_slots:
            self.time_slots[date_key] = []
            self.booked_slots[date_key] = []
        
        # Generate time slots
        start_hour, start_min = map(int, start_time.split(':'))
        end_hour, end_min = map(int, end_time.split(':'))
        
        current_time = datetime.combine(date_key, datetime.min.time().replace(hour=start_hour, minute=start_min))
        end_time_obj = datetime.combine(date_key, datetime.min.time().replace(hour=end_hour, minute=end_min))
        
        while current_time < end_time_obj:
            self.time_slots[date_key].append(current_time.strftime('%H:%M'))
            current_time += timedelta(minutes=slot_duration)
    
    def book_slot(self, date: datetime, time: str) -> bool:
        """Book a time slot"""
        date_key = date.date()
        if date_key in self.time_slots and time in self.time_slots[date_key]:
            if date_key not in self.booked_slots:
                self.booked_slots[date_key] = []
            if time not in self.booked_slots[date_key]:
                self.booked_slots[date_key].append(time)
                return True
        return False
    
    def get_available_slots(self, date: datetime) -> List[str]:
        """Get available time slots for a date"""
        date_key = date.date()
        if date_key not in self.time_slots:
            return []
        
        booked = self.booked_slots.get(date_key, [])
        return [slot for slot in self.time_slots[date_key] if slot not in booked]

class Doctor(User):
    def __init__(self, user_id: str, name: str, email: str, password: str,
                 specialization: str, license_number: str, years_experience: int):
        super().__init__(user_id, name, email, password, "Doctor")
        self.specialization = specialization
        self.license_number = license_number
        self.years_experience = years_experience
        self.schedule = Schedule()
        self.assigned_patients: List[str] = []  # List of patient IDs
        self.appointments: List[Appointment] = []
        self.consultation_fee = 0.0
        self.rating = 0.0
        self.reviews = []
        self.qualifications = []
        self.hospital_id = None
    
    def add_qualification(self, qualification: str, institution: str, year: int):
        """Add a qualification to doctor's profile"""
        self.qualifications.append({
            'qualification': qualification,
            'institution': institution,
            'year': year
        })
    
    def set_availability(self, date: datetime, start_time: str, end_time: str):
        """Set availability for a specific date"""
        self.schedule.add_availability(date, start_time, end_time)
    
    def view_schedule(self, date: datetime = None) -> Dict:
        """View schedule for a specific date or all dates"""
        if date:
            date_key = date.date()
            return {
                date_key: {
                    'available_slots': self.schedule.get_available_slots(date),
                    'booked_slots': self.schedule.booked_slots.get(date_key, [])
                }
            }
        return {
            'time_slots': self.schedule.time_slots,
            'booked_slots': self.schedule.booked_slots
        }
    
    def add_patient(self, patient_id: str):
        """Assign a patient to this doctor"""
        if patient_id not in self.assigned_patients:
            self.assigned_patients.append(patient_id)
    
    def remove_patient(self, patient_id: str):
        """Remove a patient from doctor's list"""
        if patient_id in self.assigned_patients:
            self.assigned_patients.remove(patient_id)
    
    def add_diagnosis(self, patient_id: str, diagnosis: str, treatment: str, 
                     medications: List[Dict] = None) -> str:
        """Add diagnosis and create medical record"""
        record_id = f"MR_{datetime.now().strftime('%Y%m%d')}_{len(self.assigned_patients):03d}"
        record = MedicalRecord(record_id, patient_id, self.user_id, diagnosis, treatment, datetime.now())
        
        if medications:
            for med in medications:
                record.add_medication(med['name'], med['dosage'], med['duration'])
        
        return record_id
    
    def manage_appointment(self, appointment_id: str, action: str, **kwargs) -> bool:
        """Manage appointment (complete, cancel, reschedule)"""
        appointment = next((apt for apt in self.appointments if apt.appointment_id == appointment_id), None)
        
        if not appointment:
            return False
        
        if action == "complete":
            diagnosis = kwargs.get('diagnosis', '')
            prescription = kwargs.get('prescription', '')
            notes = kwargs.get('notes', '')
            appointment.complete_appointment(diagnosis, prescription, notes)
            return True
        elif action == "cancel":
            appointment.cancel_appointment()
            return True
        elif action == "reschedule":
            new_date = kwargs.get('new_date')
            if new_date:
                appointment.date = new_date
                return True
        
        return False
    
    def get_patient_history(self, patient_id: str) -> List[MedicalRecord]:
        """Get medical history for a specific patient"""
        # This would typically query a database
        # For now, returning empty list as placeholder
        return []
    
    def add_appointment(self, appointment: Appointment):
        """Add an appointment to doctor's schedule"""
        self.appointments.append(appointment)
        # Book the time slot
        self.schedule.book_slot(appointment.date, appointment.date.strftime('%H:%M'))
    
    def get_dashboard_data(self) -> Dict:
        """Return doctor dashboard data"""
        today = datetime.now().date()
        today_appointments = [apt for apt in self.appointments 
                            if apt.date.date() == today and apt.status == "scheduled"]
        
        pending_appointments = [apt for apt in self.appointments 
                              if apt.status == "scheduled" and apt.date > datetime.now()]
        
        completed_today = [apt for apt in self.appointments 
                         if apt.date.date() == today and apt.status == "completed"]
        
        return {
            "user_info": {
                "name": self.name,
                "specialization": self.specialization,
                "experience": f"{self.years_experience} years",
                "rating": self.rating
            },
            "today_appointments": len(today_appointments),
            "pending_appointments": len(pending_appointments),
            "completed_today": len(completed_today),
            "total_patients": len(self.assigned_patients),
            "next_appointment": today_appointments[0] if today_appointments else None,
            "consultation_fee": self.consultation_fee
        }
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization} (ID: {self.user_id})"
