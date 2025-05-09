# Hospital Management System

A web-based hospital management system built with Flask that manages OPD, IPD, OT, and Delivery records.

## Features

- User Authentication
- Patient Registration
- OPD Records Management
- IPD Records Management
- OT Records Management
- Delivery Records Management
- Responsive Web Interface

## Technology Stack

- Python 3.8+
- Flask
- SQLAlchemy
- Bootstrap 5
- SQLite Database

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/hssling/HospitalRecords.git
cd HospitalRecords
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5001`

## Default Admin Credentials

- Username: admin
- Password: admin123

## Project Structure

```
HospitalRecords/
├── app.py              # Main application file
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS, images)
└── templates/         # HTML templates
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── patient_register.html
    ├── opd_records.html
    ├── ipd_records.html
    ├── ot_records.html
    └── delivery_records.html
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 