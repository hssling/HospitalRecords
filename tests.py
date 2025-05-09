import unittest
from app import app, db, User, Patient, OPDRecord, IPDRecord, OTRecord, DeliveryRecord
from config import TestingConfig
import json

class HospitalManagementTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestingConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        user = User(username='testuser', role='admin')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        
        # Login
        self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_patient_registration(self):
        response = self.app.post('/register_patient', data={
            'patient_id': 'PAT001',
            'name': 'Test Patient',
            'age': 30,
            'gender': 'Male',
            'contact': '1234567890'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
        patient = Patient.query.filter_by(patient_id='PAT001').first()
        self.assertIsNotNone(patient)
        self.assertEqual(patient.name, 'Test Patient')

    def test_opd_record_creation(self):
        # First create a patient
        patient = Patient(patient_id='PAT001', name='Test Patient', age=30, gender='Male', contact='1234567890')
        db.session.add(patient)
        db.session.commit()
        
        # Create OPD record
        response = self.app.post('/api/opd', json={
            'patient_id': 'PAT001',
            'department': 'General',
            'doctor': 'Dr. Test',
            'diagnosis': 'Test Diagnosis',
            'treatment': 'Test Treatment',
            'fee': 100.00
        })
        self.assertEqual(response.status_code, 200)
        
        record = OPDRecord.query.filter_by(patient_id='PAT001').first()
        self.assertIsNotNone(record)
        self.assertEqual(record.department, 'General')

    def test_ipd_record_creation(self):
        # First create a patient
        patient = Patient(patient_id='PAT001', name='Test Patient', age=30, gender='Male', contact='1234567890')
        db.session.add(patient)
        db.session.commit()
        
        # Create IPD record
        response = self.app.post('/api/ipd', json={
            'patient_id': 'PAT001',
            'admission_date': '2024-01-01',
            'room_no': '101',
            'admission_reason': 'Test Admission',
            'doctor': 'Dr. Test',
            'status': 'Admitted'
        })
        self.assertEqual(response.status_code, 200)
        
        record = IPDRecord.query.filter_by(patient_id='PAT001').first()
        self.assertIsNotNone(record)
        self.assertEqual(record.room_no, '101')

    def test_ot_record_creation(self):
        # First create a patient
        patient = Patient(patient_id='PAT001', name='Test Patient', age=30, gender='Male', contact='1234567890')
        db.session.add(patient)
        db.session.commit()
        
        # Create OT record
        response = self.app.post('/api/ot', json={
            'patient_id': 'PAT001',
            'date': '2024-01-01',
            'surgery_type': 'Test Surgery',
            'surgeon': 'Dr. Test',
            'anesthetist': 'Dr. Anesthesia',
            'start_time': '2024-01-01 10:00',
            'end_time': '2024-01-01 12:00',
            'status': 'Scheduled'
        })
        self.assertEqual(response.status_code, 200)
        
        record = OTRecord.query.filter_by(patient_id='PAT001').first()
        self.assertIsNotNone(record)
        self.assertEqual(record.surgery_type, 'Test Surgery')

    def test_delivery_record_creation(self):
        # First create a patient
        patient = Patient(patient_id='PAT001', name='Test Patient', age=30, gender='Female', contact='1234567890')
        db.session.add(patient)
        db.session.commit()
        
        # Create Delivery record
        response = self.app.post('/api/delivery', json={
            'patient_id': 'PAT001',
            'date': '2024-01-01',
            'delivery_type': 'Normal',
            'doctor': 'Dr. Test',
            'baby_gender': 'Male',
            'weight': 3.5,
            'status': 'Completed'
        })
        self.assertEqual(response.status_code, 200)
        
        record = DeliveryRecord.query.filter_by(patient_id='PAT001').first()
        self.assertIsNotNone(record)
        self.assertEqual(record.delivery_type, 'Normal')

if __name__ == '__main__':
    unittest.main() 