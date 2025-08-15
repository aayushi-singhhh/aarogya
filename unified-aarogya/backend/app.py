from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
client = MongoClient(mongo_uri)
db = client[db_name]

print("✅ Connected to MongoDB")


@app.route("/testdb")
def testdb():
    test_data = {"name": "Test Patient", "age": 30}
    db.patients.insert_one(test_data)
    return {"message": "Data inserted into MongoDB!"}

#!/usr/bin/env python3
"""
Flask Web Application for Hospital Portal System
This creates a web interface for the hospital portal system
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import sys
import os

# Add the current directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.patient import Patient, MedicalRecord
from models.doctor import Doctor
from models.hospital_admin import HospitalAdmin
from portal_system import HospitalPortalSystem

app = Flask(__name__)
app.secret_key = 'aarogya_hospital_portal_secret_key_2025'

# Enable CORS for frontend integration
CORS(app, origins=[
    'http://localhost:5173', 
    'http://localhost:5174', 
    'http://localhost:3000',
    'https://aarogya-jv3xifct7-aayushi-singhhs-projects.vercel.app',
    'https://aarogya-aayushi-singhhs-projects.vercel.app',
    'https://aarogya.vercel.app'
], supports_credentials=True)

# Initialize the portal system
portal_system = HospitalPortalSystem()

@app.route('/')
def home():
    """Home page with login options"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = portal_system.auth_system.login(email, password)
        if user:
            session['user_id'] = user.user_id
            session['user_role'] = user.role
            session['user_name'] = user.name
            
            # Redirect based on role
            if user.role == 'Patient':
                return redirect(url_for('patient_dashboard'))
            elif user.role == 'Doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user.role == 'Hospital Admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    portal_system.auth_system.logout()
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/demo_data')
def initialize_demo():
    """Initialize demo data"""
    portal_system.initialize_demo_data()
    flash('Demo data initialized successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/patient/dashboard')
def patient_dashboard():
    """Patient dashboard"""
    if 'user_id' not in session or session.get('user_role') != 'Patient':
        return redirect(url_for('login'))
    
    user = portal_system.auth_system.get_current_user()
    if not user:
        # Find user by ID
        for system_user in portal_system.auth_system.users.values():
            if system_user.user_id == session['user_id']:
                user = system_user
                break
    
    if user:
        dashboard_data = user.get_dashboard_data()
        appointments = user.view_appointments()
        medical_records = user.view_medical_reports()
        
        return render_template('patient_dashboard.html', 
                             user=user, 
                             dashboard=dashboard_data,
                             appointments=appointments,
                             medical_records=medical_records)
    
    return redirect(url_for('login'))

@app.route('/doctor/dashboard')
def doctor_dashboard():
    """Doctor dashboard"""
    if 'user_id' not in session or session.get('user_role') != 'Doctor':
        return redirect(url_for('login'))
    
    user = portal_system.auth_system.get_current_user()
    if not user:
        # Find user by ID
        for system_user in portal_system.auth_system.users.values():
            if system_user.user_id == session['user_id']:
                user = system_user
                break
    
    if user:
        dashboard_data = user.get_dashboard_data()
        appointments = user.appointments
        
        return render_template('doctor_dashboard.html', 
                             user=user, 
                             dashboard=dashboard_data,
                             appointments=appointments)
    
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'user_id' not in session or session.get('user_role') != 'Hospital Admin':
        return redirect(url_for('login'))
    
    user = portal_system.auth_system.get_current_user()
    if not user:
        # Find user by ID
        for system_user in portal_system.auth_system.users.values():
            if system_user.user_id == session['user_id']:
                user = system_user
                break
    
    if user:
        dashboard_data = user.get_dashboard_data()
        hospital_data = user.view_hospital_data()
        
        return render_template('admin_dashboard.html', 
                             user=user, 
                             dashboard=dashboard_data,
                             hospital_data=hospital_data)
    
    return redirect(url_for('login'))

@app.route('/patient/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    """Book appointment page"""
    if 'user_id' not in session or session.get('user_role') != 'Patient':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        reason = request.form['reason']
        
        # For demo, book for tomorrow
        apt_date = datetime.now() + timedelta(days=1, hours=10)
        
        # Find patient
        patient = None
        for user in portal_system.auth_system.users.values():
            if user.user_id == session['user_id'] and isinstance(user, Patient):
                patient = user
                break
        
        if patient:
            apt_id = patient.book_appointment(doctor_id, apt_date, reason)
            flash(f'Appointment booked successfully! ID: {apt_id}', 'success')
            return redirect(url_for('patient_dashboard'))
    
    # Get available doctors
    admin = None
    for user in portal_system.auth_system.users.values():
        if isinstance(user, HospitalAdmin):
            admin = user
            break
    
    doctors = admin.managed_doctors if admin else []
    
    return render_template('book_appointment.html', doctors=doctors)

@app.route('/api/user_info')
def api_user_info():
    """API endpoint to get current user info"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    return jsonify({
        'user_id': session.get('user_id'),
        'role': session.get('user_role'),
        'name': session.get('user_name')
    })

@app.route('/test-db')
def test_db():
    return {"status": "ok"}


if __name__ == '__main__':
    print("🏥 Starting Aarogya Hospital Portal Backend...")
    print("📍 Server running at: http://localhost:5001")
    print("🔗 Frontend integration enabled for: http://localhost:5174")
    app.run(debug=True, port=5001, host='0.0.0.0')
