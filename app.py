from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# Define paths to JSON files
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), 'users.json')
APPOINTMENTS_FILE = os.path.join(os.path.dirname(__file__), 'appointments.json')

# Function to read JSON files
def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Convert date strings back to date objects
            for key in list(data.keys()):
                try:
                    date_key = datetime.strptime(key, '%Y-%m-%d').date()
                    data[date_key] = data.pop(key)
                except ValueError:
                    # If there's a date parsing issue, skip conversion
                    continue
            return data
    return {}

# Function to write to JSON files
def write_json_file(file_path, data):
    # Convert date objects to strings
    data_str = {date.isoformat(): appointments for date, appointments in data.items()}
    with open(file_path, 'w') as file:
        json.dump(data_str, file, indent=4)

# Load existing users and appointments
USERS = read_json_file(USER_DATA_FILE)
APPOINTMENTS = read_json_file(APPOINTMENTS_FILE)

# Serve the login page when the root URL is accessed
@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

# Handle the login form submission
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = USERS.get(email)
    if user and user.get('password') == password:
        role = user.get('role')
        if role == 'receptionist':
            return redirect(url_for('receptionist_add'))
        elif role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
    else:
        return render_template('login.html', error="Invalid email or password!")

# Serve the Receptionist Add Appointment Page
@app.route('/receptionist/add', methods=['GET'])
def receptionist_add():
    return render_template('add_appointment.html')

# Handle adding an appointment
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_name = request.form.get('patientName')
    appointment_date = request.form.get('appointmentDate')

    # Validate date format
    try:
        appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format!'}), 400

    if not patient_name or not appointment_date:
        return jsonify({'message': 'Missing fields!'}), 400

    # Load existing appointments
    appointments = read_json_file(APPOINTMENTS_FILE)
    
    # Add new appointment
    if appointment_date not in appointments:
        appointments[appointment_date] = []
    appointments[appointment_date].append(patient_name)

    # Save updated appointments
    write_json_file(APPOINTMENTS_FILE, appointments)

    return redirect(url_for('receptionist_view'))

# Serve the Receptionist View Appointments Page
@app.route('/receptionist/view', methods=['GET'])
def receptionist_view():
    return render_template('view_appointments.html')

# Handle viewing today's appointments
@app.route('/todays_appointments', methods=['GET'])
def todays_appointments():
    today = datetime.now().date()
    appointments = read_json_file(APPOINTMENTS_FILE)
    todays_appointments = appointments.get(today, [])
    return jsonify(todays_appointments)

# Serve the Doctor Dashboard
@app.route('/doctor', methods=['GET'])
def doctor_dashboard():
    appointments = read_json_file(APPOINTMENTS_FILE)
    return render_template('doctor.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
