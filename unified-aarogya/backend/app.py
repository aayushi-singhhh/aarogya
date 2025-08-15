from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import sys

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = 'aarogya_hospital_portal_secret_key_2025'

# Enable CORS for frontend integration
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:3000",
            "https://aarogya-jv3xifct7-aayushi-singhhs-projects.vercel.app",
            "https://aarogya-aayushi-singhhs-projects.vercel.app",
            "https://aarogya.vercel.app"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

if not mongo_uri or not db_name:
    raise ValueError("❌ MONGO_URI or DB_NAME is not set in your .env file.")

client = MongoClient(mongo_uri)
db = client[db_name]
print("✅ Connected to MongoDB")

# Add the current directory to path so we can import our models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.patient import Patient, MedicalRecord
from models.doctor import Doctor
from models.hospital_admin import HospitalAdmin
from portal_system import HospitalPortalSystem

# Initialize the portal system
portal_system = HospitalPortalSystem()

# ---------------- ROUTES ---------------- #

@app.route("/testdb")
def testdb():
    """Test inserting data into MongoDB"""
    test_data = {"name": "Test Patient", "age": 30}
    db.patients.insert_one(test_data)
    return {"message": "Data inserted into MongoDB!"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = portal_system.auth_system.login(email, password)
        if user:
            session['user_id'] = user.user_id
            session['user_role'] = user.role
            session['user_name'] = user.name
            
            if user.role == 'Patient':
                return redirect(url_for('patient_dashboard'))
            elif user.role == 'Doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user.role == 'Hospital Admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html')

@app.route('/register/patient', methods=['POST'])
def register_patient():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        age = data.get('age')
        gender = data.get('gender')
        phone = data.get('phone')
        
        # Validate required fields
        if not all([name, email, password, age, gender, phone]):
            return jsonify({'error': 'Missing required fields'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    try:
        # Check if email already exists
        if any(user.email == email for user in portal_system.auth_system.users.values()):
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new patient
        new_patient = Patient(
            user_id=f"PAT{len(portal_system.auth_system.users) + 1}",
            name=name,
            email=email,
            password=password,
            age=age,
            gender=gender,
            phone=phone
        )
        
        # Add to portal system
        portal_system.auth_system.users[new_patient.user_id] = new_patient
        return jsonify({'message': 'Patient registered successfully', 'user_id': new_patient.user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register/doctor', methods=['POST'])
def register_doctor():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    specialization = data.get('specialization')
    experience = data.get('experience')
    
    try:
        # Check if email already exists
        if any(user.email == email for user in portal_system.auth_system.users.values()):
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new doctor
        new_doctor = Doctor(
            user_id=f"DOC{len(portal_system.auth_system.users) + 1}",
            name=name,
            email=email,
            password=password,
            specialization=specialization,
            experience=experience
        )
        
        # Add to portal system
        portal_system.auth_system.users[new_doctor.user_id] = new_doctor
        return jsonify({'message': 'Doctor registered successfully', 'user_id': new_doctor.user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register/admin', methods=['POST'])
def register_admin():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    hospital_name = data.get('hospital_name')
    
    try:
        # Check if email already exists
        if any(user.email == email for user in portal_system.auth_system.users.values()):
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new admin
        new_admin = HospitalAdmin(
            user_id=f"ADM{len(portal_system.auth_system.users) + 1}",
            name=name,
            email=email,
            password=password,
            hospital_name=hospital_name
        )
        
        # Add to portal system
        portal_system.auth_system.users[new_admin.user_id] = new_admin
        return jsonify({'message': 'Admin registered successfully', 'user_id': new_admin.user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    portal_system.auth_system.logout()
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/demo_data')
def initialize_demo():
    portal_system.initialize_demo_data()
    flash('Demo data initialized successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/patient/dashboard')
def patient_dashboard():
    if 'user_id' not in session or session.get('user_role') != 'Patient':
        return redirect(url_for('login'))
    
    user = portal_system.auth_system.get_current_user()
    if not user:
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
    if 'user_id' not in session or session.get('user_role') != 'Doctor':
        return redirect(url_for('login'))
    
    user = portal_system.auth_system.get_current_user()
    if not user:
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
    if 'user_id' not in session or session.get('user_role') != 'Hospital Admin':
        return redirect(url_for('login'))
    
    user = portal_system.auth_system.get_current_user()
    if not user:
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
    if 'user_id' not in session or session.get('user_role') != 'Patient':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        reason = request.form['reason']
        
        apt_date = datetime.now() + timedelta(days=1, hours=10)
        
        patient = None
        for user in portal_system.auth_system.users.values():
            if user.user_id == session['user_id'] and isinstance(user, Patient):
                patient = user
                break
        
        if patient:
            apt_id = patient.book_appointment(doctor_id, apt_date, reason)
            flash(f'Appointment booked successfully! ID: {apt_id}', 'success')
            return redirect(url_for('patient_dashboard'))
    
    admin = None
    for user in portal_system.auth_system.users.values():
        if isinstance(user, HospitalAdmin):
            admin = user
            break
    
    doctors = admin.managed_doctors if admin else []
    return render_template('book_appointment.html', doctors=doctors)

@app.route('/api/user_info')
def api_user_info():
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

# ---------------- MAIN ---------------- #
if __name__ == '__main__':
    print("🏥 Starting Aarogya Hospital Portal Backend...")
    print("📍 Server running at: http://localhost:5001")
    print("🔗 Frontend integration enabled for: http://localhost:5174")
    app.run(debug=True, port=5001, host='0.0.0.0')
