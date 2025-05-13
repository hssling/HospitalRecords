from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

hospital_management_system = Flask(__name__)
hospital_management_system.config['SECRET_KEY'] = os.urandom(24)
hospital_management_system.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
hospital_management_system.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(hospital_management_system)
login_manager = LoginManager()
login_manager.init_app(hospital_management_system)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(20))

class OPDRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient_id = db.Column(db.String(20), db.ForeignKey('patient.patient_id'))
    department = db.Column(db.String(50))
    doctor = db.Column(db.String(100))
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    fee = db.Column(db.Float)

class IPDRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admission_date = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(db.String(20), db.ForeignKey('patient.patient_id'))
    room_no = db.Column(db.String(20))
    admission_reason = db.Column(db.Text)
    doctor = db.Column(db.String(100))
    discharge_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))

class OTRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(db.String(20), db.ForeignKey('patient.patient_id'))
    surgery_type = db.Column(db.String(100))
    surgeon = db.Column(db.String(100))
    anesthetist = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20))

class DeliveryRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(db.String(20), db.ForeignKey('patient.patient_id'))
    delivery_type = db.Column(db.String(50))
    doctor = db.Column(db.String(100))
    baby_gender = db.Column(db.String(10))
    weight = db.Column(db.Float)
    status = db.Column(db.String(20))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@hospital_management_system.route('/')
def index():
    return render_template('index.html')

@hospital_management_system.route('/test')
def test():
    return "Server is running!"

@hospital_management_system.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@hospital_management_system.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@hospital_management_system.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Patient Registration
@hospital_management_system.route('/register_patient', methods=['GET', 'POST'])
@login_required
def register_patient():
    if request.method == 'POST':
        patient = Patient(
            patient_id=request.form['patient_id'],
            name=request.form['name'],
            age=request.form['age'],
            gender=request.form['gender'],
            contact=request.form['contact']
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient registered successfully!')
        return redirect(url_for('dashboard'))
    return render_template('patient_register.html')

# Department Record Routes
@hospital_management_system.route('/opd_records')
@login_required
def opd_records():
    return render_template('opd_records.html')

@hospital_management_system.route('/ipd_records')
@login_required
def ipd_records():
    return render_template('ipd_records.html')

@hospital_management_system.route('/ot_records')
@login_required
def ot_records():
    return render_template('ot_records.html')

@hospital_management_system.route('/delivery_records')
@login_required
def delivery_records():
    return render_template('delivery_records.html')

# API Routes for Records
@hospital_management_system.route('/api/opd', methods=['GET', 'POST'])
@login_required
def opd_records_api():
    if request.method == 'POST':
        data = request.json
        new_record = OPDRecord(
            patient_id=data['patient_id'],
            department=data['department'],
            doctor=data['doctor'],
            diagnosis=data['diagnosis'],
            treatment=data['treatment'],
            fee=float(data['fee'])
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Record added successfully'})
    
    records = OPDRecord.query.all()
    return jsonify([{
        'id': r.id,
        'date': r.date.strftime('%Y-%m-%d'),
        'patient_id': r.patient_id,
        'department': r.department,
        'doctor': r.doctor,
        'diagnosis': r.diagnosis,
        'treatment': r.treatment,
        'fee': r.fee
    } for r in records])

@hospital_management_system.route('/api/ipd', methods=['GET', 'POST'])
@login_required
def ipd_records_api():
    if request.method == 'POST':
        data = request.json
        new_record = IPDRecord(
            admission_date=datetime.strptime(data['admission_date'], '%Y-%m-%d'),
            patient_id=data['patient_id'],
            room_no=data['room_no'],
            admission_reason=data['admission_reason'],
            doctor=data['doctor'],
            status=data['status']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Record added successfully'})
    
    records = IPDRecord.query.all()
    return jsonify([{
        'id': r.id,
        'admission_date': r.admission_date.strftime('%Y-%m-%d'),
        'patient_id': r.patient_id,
        'room_no': r.room_no,
        'admission_reason': r.admission_reason,
        'doctor': r.doctor,
        'discharge_date': r.discharge_date.strftime('%Y-%m-%d') if r.discharge_date else None,
        'status': r.status
    } for r in records])

@hospital_management_system.route('/api/ot', methods=['GET', 'POST'])
@login_required
def ot_records_api():
    if request.method == 'POST':
        data = request.json
        new_record = OTRecord(
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            patient_id=data['patient_id'],
            surgery_type=data['surgery_type'],
            surgeon=data['surgeon'],
            anesthetist=data['anesthetist'],
            start_time=datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M'),
            end_time=datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M'),
            status=data['status']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Record added successfully'})
    
    records = OTRecord.query.all()
    return jsonify([{
        'id': r.id,
        'date': r.date.strftime('%Y-%m-%d'),
        'patient_id': r.patient_id,
        'surgery_type': r.surgery_type,
        'surgeon': r.surgeon,
        'anesthetist': r.anesthetist,
        'start_time': r.start_time.strftime('%Y-%m-%d %H:%M'),
        'end_time': r.end_time.strftime('%Y-%m-%d %H:%M'),
        'status': r.status
    } for r in records])

@hospital_management_system.route('/api/delivery', methods=['GET', 'POST'])
@login_required
def delivery_records_api():
    if request.method == 'POST':
        data = request.json
        new_record = DeliveryRecord(
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            patient_id=data['patient_id'],
            delivery_type=data['delivery_type'],
            doctor=data['doctor'],
            baby_gender=data['baby_gender'],
            weight=float(data['weight']),
            status=data['status']
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': 'Record added successfully'})
    
    records = DeliveryRecord.query.all()
    return jsonify([{
        'id': r.id,
        'date': r.date.strftime('%Y-%m-%d'),
        'patient_id': r.patient_id,
        'delivery_type': r.delivery_type,
        'doctor': r.doctor,
        'baby_gender': r.baby_gender,
        'weight': r.weight,
        'status': r.status
    } for r in records])

if __name__ == '__main__':
    with hospital_management_system.app_context():
        db.create_all()
    hospital_management_system.run(debug=True, host='127.0.0.1', port=5001) 