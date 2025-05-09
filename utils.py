import os
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
from flask import current_app

def allowed_file(filename):
    """Check if the file extension is allowed"""
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    """Save uploaded file securely"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return file_path
    return None

def import_patient_data(file_path):
    """Import patient data from Excel/CSV file"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # Validate required columns
        required_columns = ['patient_id', 'name', 'age', 'gender', 'contact']
        if not all(col in df.columns for col in required_columns):
            return False, "Missing required columns"
        
        return True, df
    except Exception as e:
        return False, str(e)

def generate_patient_id():
    """Generate a unique patient ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"PAT{timestamp}"

def format_currency(amount):
    """Format amount as currency"""
    return f"₹{amount:,.2f}"

def calculate_age(birth_date):
    """Calculate age from birth date"""
    today = datetime.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def validate_phone_number(phone):
    """Validate phone number format"""
    import re
    pattern = r'^\+?1?\d{9,15}$'
    return bool(re.match(pattern, phone))

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def get_patient_summary(patient_id):
    """Get summary of patient's medical history"""
    from app import db, OPDRecord, IPDRecord, OTRecord, DeliveryRecord
    
    summary = {
        'opd_visits': OPDRecord.query.filter_by(patient_id=patient_id).count(),
        'ipd_admissions': IPDRecord.query.filter_by(patient_id=patient_id).count(),
        'surgeries': OTRecord.query.filter_by(patient_id=patient_id).count(),
        'deliveries': DeliveryRecord.query.filter_by(patient_id=patient_id).count()
    }
    
    return summary

def export_to_excel(data, filename):
    """Export data to Excel file"""
    df = pd.DataFrame(data)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    df.to_excel(file_path, index=False)
    return file_path 