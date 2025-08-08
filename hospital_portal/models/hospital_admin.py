from datetime import datetime
from typing import List, Dict, Optional
from .user import User
from .patient import Patient
from .doctor import Doctor

class HospitalStats:
    def __init__(self):
        self.total_patients = 0
        self.total_doctors = 0
        self.total_appointments = 0
        self.departments = {}
        self.monthly_revenue = 0.0
        self.bed_occupancy = 0
        self.total_beds = 0
    
    def update_stats(self, patients: List[Patient], doctors: List[Doctor]):
        """Update hospital statistics"""
        self.total_patients = len(patients)
        self.total_doctors = len(doctors)
        
        # Count appointments
        self.total_appointments = sum(len(patient.appointments) for patient in patients)
        
        # Count doctors by department/specialization
        self.departments = {}
        for doctor in doctors:
            spec = doctor.specialization
            if spec not in self.departments:
                self.departments[spec] = 0
            self.departments[spec] += 1

class HospitalAdmin(User):
    def __init__(self, user_id: str, name: str, email: str, password: str, 
                 admin_level: str = "senior"):
        super().__init__(user_id, name, email, password, "Hospital Admin")
        self.admin_level = admin_level  # junior, senior, super
        self.managed_doctors: List[Doctor] = []
        self.managed_patients: List[Patient] = []
        self.hospital_stats = HospitalStats()
        self.permissions = self._set_permissions()
        self.departments_managed = []
    
    def _set_permissions(self) -> Dict[str, bool]:
        """Set permissions based on admin level"""
        base_permissions = {
            "view_patients": True,
            "view_doctors": True,
            "view_appointments": True,
            "view_reports": True
        }
        
        if self.admin_level == "senior":
            base_permissions.update({
                "add_doctor": True,
                "remove_doctor": False,
                "modify_schedules": True,
                "assign_patients": True,
                "view_financial_data": True
            })
        elif self.admin_level == "super":
            base_permissions.update({
                "add_doctor": True,
                "remove_doctor": True,
                "modify_schedules": True,
                "assign_patients": True,
                "view_financial_data": True,
                "manage_admins": True,
                "system_settings": True
            })
        
        return base_permissions
    
    def add_doctor(self, doctor: Doctor) -> bool:
        """Add a new doctor to the hospital"""
        if not self.permissions.get("add_doctor", False):
            print("Access denied: Insufficient permissions to add doctors")
            return False
        
        if doctor not in self.managed_doctors:
            self.managed_doctors.append(doctor)
            doctor.hospital_id = "HOSP_001"  # Placeholder hospital ID
            print(f"Doctor {doctor.name} added successfully")
            return True
        return False
    
    def remove_doctor(self, doctor_id: str) -> bool:
        """Remove a doctor from the hospital"""
        if not self.permissions.get("remove_doctor", False):
            print("Access denied: Insufficient permissions to remove doctors")
            return False
        
        doctor = self.find_doctor_by_id(doctor_id)
        if doctor:
            self.managed_doctors.remove(doctor)
            print(f"Doctor {doctor.name} removed successfully")
            return True
        return False
    
    def add_patient(self, patient: Patient) -> bool:
        """Register a new patient"""
        if patient not in self.managed_patients:
            self.managed_patients.append(patient)
            print(f"Patient {patient.name} registered successfully")
            return True
        return False
    
    def assign_doctor_to_patient(self, patient_id: str, doctor_id: str) -> bool:
        """Assign a doctor to a patient"""
        if not self.permissions.get("assign_patients", False):
            print("Access denied: Insufficient permissions to assign patients")
            return False
        
        patient = self.find_patient_by_id(patient_id)
        doctor = self.find_doctor_by_id(doctor_id)
        
        if patient and doctor:
            doctor.add_patient(patient_id)
            print(f"Assigned Dr. {doctor.name} to patient {patient.name}")
            return True
        return False
    
    def find_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        """Find a doctor by their ID"""
        return next((doc for doc in self.managed_doctors if doc.user_id == doctor_id), None)
    
    def find_patient_by_id(self, patient_id: str) -> Optional[Patient]:
        """Find a patient by their ID"""
        return next((pat for pat in self.managed_patients if pat.user_id == patient_id), None)
    
    def find_doctor_by_specialization(self, specialization: str) -> List[Doctor]:
        """Find doctors by specialization"""
        return [doc for doc in self.managed_doctors if doc.specialization.lower() == specialization.lower()]
    
    def view_hospital_data(self) -> Dict:
        """View comprehensive hospital data"""
        if not self.permissions.get("view_reports", False):
            print("Access denied: Insufficient permissions to view hospital data")
            return {}
        
        self.hospital_stats.update_stats(self.managed_patients, self.managed_doctors)
        
        # Calculate appointment statistics
        total_appointments = sum(len(patient.appointments) for patient in self.managed_patients)
        completed_appointments = sum(
            len([apt for apt in patient.appointments if apt.status == "completed"]) 
            for patient in self.managed_patients
        )
        
        # Doctor utilization
        doctor_utilization = {}
        for doctor in self.managed_doctors:
            doctor_utilization[doctor.name] = {
                "total_patients": len(doctor.assigned_patients),
                "appointments": len(doctor.appointments),
                "specialization": doctor.specialization
            }
        
        return {
            "hospital_stats": {
                "total_patients": len(self.managed_patients),
                "total_doctors": len(self.managed_doctors),
                "total_appointments": total_appointments,
                "completed_appointments": completed_appointments,
                "departments": self.hospital_stats.departments
            },
            "doctor_utilization": doctor_utilization,
            "recent_registrations": [
                {"name": p.name, "date": p.created_at.strftime('%Y-%m-%d')} 
                for p in sorted(self.managed_patients, key=lambda x: x.created_at, reverse=True)[:5]
            ]
        }
    
    def generate_report(self, report_type: str, **kwargs) -> Dict:
        """Generate various types of reports"""
        if not self.permissions.get("view_reports", False):
            print("Access denied: Insufficient permissions to generate reports")
            return {}
        
        reports = {
            "patient_summary": self._generate_patient_report,
            "doctor_performance": self._generate_doctor_report,
            "appointment_analytics": self._generate_appointment_report,
            "department_analysis": self._generate_department_report
        }
        
        if report_type in reports:
            return reports[report_type](**kwargs)
        return {"error": "Invalid report type"}
    
    def _generate_patient_report(self, **kwargs) -> Dict:
        """Generate patient summary report"""
        age_groups = {"0-18": 0, "19-35": 0, "36-50": 0, "51-65": 0, "65+": 0}
        gender_distribution = {"Male": 0, "Female": 0, "Other": 0}
        
        for patient in self.managed_patients:
            # Age grouping
            if patient.age <= 18:
                age_groups["0-18"] += 1
            elif patient.age <= 35:
                age_groups["19-35"] += 1
            elif patient.age <= 50:
                age_groups["36-50"] += 1
            elif patient.age <= 65:
                age_groups["51-65"] += 1
            else:
                age_groups["65+"] += 1
            
            # Gender distribution
            gender_distribution[patient.gender] = gender_distribution.get(patient.gender, 0) + 1
        
        return {
            "total_patients": len(self.managed_patients),
            "age_distribution": age_groups,
            "gender_distribution": gender_distribution,
            "patients_with_allergies": len([p for p in self.managed_patients if p.allergies])
        }
    
    def _generate_doctor_report(self, **kwargs) -> Dict:
        """Generate doctor performance report"""
        return {
            "total_doctors": len(self.managed_doctors),
            "specializations": list(set(doc.specialization for doc in self.managed_doctors)),
            "average_experience": sum(doc.years_experience for doc in self.managed_doctors) / len(self.managed_doctors) if self.managed_doctors else 0,
            "doctors_by_specialization": {
                spec: len([doc for doc in self.managed_doctors if doc.specialization == spec])
                for spec in set(doc.specialization for doc in self.managed_doctors)
            }
        }
    
    def _generate_appointment_report(self, **kwargs) -> Dict:
        """Generate appointment analytics report"""
        all_appointments = []
        for patient in self.managed_patients:
            all_appointments.extend(patient.appointments)
        
        status_count = {"scheduled": 0, "completed": 0, "cancelled": 0}
        for apt in all_appointments:
            status_count[apt.status] = status_count.get(apt.status, 0) + 1
        
        return {
            "total_appointments": len(all_appointments),
            "appointment_status": status_count,
            "completion_rate": (status_count["completed"] / len(all_appointments) * 100) if all_appointments else 0
        }
    
    def _generate_department_report(self, **kwargs) -> Dict:
        """Generate department analysis report"""
        departments = {}
        for doctor in self.managed_doctors:
            dept = doctor.specialization
            if dept not in departments:
                departments[dept] = {
                    "doctors": 0,
                    "patients": 0,
                    "appointments": 0
                }
            
            departments[dept]["doctors"] += 1
            departments[dept]["patients"] += len(doctor.assigned_patients)
            departments[dept]["appointments"] += len(doctor.appointments)
        
        return {"departments": departments}
    
    def get_dashboard_data(self) -> Dict:
        """Return admin dashboard data"""
        self.hospital_stats.update_stats(self.managed_patients, self.managed_doctors)
        
        today = datetime.now().date()
        today_appointments = []
        for patient in self.managed_patients:
            today_appointments.extend([
                apt for apt in patient.appointments 
                if apt.date.date() == today
            ])
        
        return {
            "user_info": {
                "name": self.name,
                "admin_level": self.admin_level,
                "departments_managed": len(self.departments_managed)
            },
            "hospital_overview": {
                "total_patients": len(self.managed_patients),
                "total_doctors": len(self.managed_doctors),
                "today_appointments": len(today_appointments),
                "departments": len(set(doc.specialization for doc in self.managed_doctors))
            },
            "recent_activity": {
                "new_patients_this_week": len([p for p in self.managed_patients 
                                             if (datetime.now() - p.created_at).days <= 7]),
                "appointments_today": len([apt for apt in today_appointments if apt.status == "scheduled"])
            }
        }
    
    def __str__(self):
        return f"Hospital Admin: {self.name} ({self.admin_level} level)"
