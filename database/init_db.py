# database/init_db.py
import sqlite3
import os

DB_FOLDER = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_FOLDER, 'hospital.db')

# Purani database file delete karo taaki fresh bane
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Users Table
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password TEXT NOT NULL,
    city TEXT
)
''')

# 2. Hospitals Table
cursor.execute('''
CREATE TABLE hospitals (
    hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_name TEXT NOT NULL,
    area TEXT,
    city TEXT,
    state TEXT,
    pincode TEXT,
    phone TEXT,
    latitude REAL,
    longitude REAL,
    rating REAL,
    emergency_24x7 INTEGER,
    opening_time TEXT,
    doctors_count INTEGER,
    beds INTEGER,
    verification_status TEXT
)
''')

# 3. Services Table
cursor.execute('''
CREATE TABLE services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id INTEGER,
    service_name TEXT NOT NULL,
    available INTEGER,
    price_inr REAL,
    price_type TEXT,
    last_updated TEXT,
    verification_status TEXT,
    FOREIGN KEY (hospital_id) REFERENCES hospitals (hospital_id)
)
''')

# 4. Bookings Table
cursor.execute('''
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    patient_name TEXT NOT NULL,
    patient_phone TEXT NOT NULL,
    hospital_name TEXT NOT NULL,
    service_name TEXT NOT NULL,
    price_inr REAL NOT NULL,
    appointment_date TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    payment_status TEXT NOT NULL,
    transaction_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Hospitals Data Insert
hospitals_data = [
    (1, 'City Care Hospital', 'Bistupur', 'Jamshedpur', 'Jharkhand', '831001', '0657-2223344', 22.8046, 86.1821, 4.5, 1, '24 Hours', 45, 120, 'Verified'),
    (2, 'Metro Multi-Speciality', 'Sakchi', 'Jamshedpur', 'Jharkhand', '831001', '0657-2334455', 22.8120, 86.2029, 4.2, 1, '24 Hours', 60, 200, 'Verified'),
    (3, 'LifeLine Health Center', 'Kadma', 'Jamshedpur', 'Jharkhand', '831005', '0657-2445566', 22.7950, 86.1650, 4.7, 1, '24 Hours', 30, 80, 'Verified'),
    (4, 'Apex Diagnostic & Clinic', 'Sonari', 'Jamshedpur', 'Jharkhand', '831011', '0657-2556677', 22.8210, 86.1680, 4.0, 0, '08:00 AM - 09:00 PM', 15, 25, 'Verified'),
    (5, 'Sunrise Super Hospital', 'Telco', 'Jamshedpur', 'Jharkhand', '831004', '0657-2667788', 22.7750, 86.2400, 4.4, 1, '24 Hours', 50, 150, 'Verified')
]
cursor.executemany('INSERT INTO hospitals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', hospitals_data)

# Services / Tests Data Insert
services_data = [
    (1, 1, 'X-Ray', 1, 350.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (2, 1, 'Blood Test', 1, 200.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (3, 1, 'CT Scan', 1, 1200.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (4, 1, 'MRI', 1, 2500.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (5, 1, 'ECG', 1, 250.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (6, 1, 'Health Checkup', 1, 999.0, 'Package', '01-Sep-2026', 'Verified'),

    (7, 2, 'X-Ray', 1, 400.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (8, 2, 'Blood Test', 1, 250.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (9, 2, 'CT Scan', 1, 1350.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (10, 2, 'MRI', 1, 2800.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (11, 2, 'ECG', 1, 300.0, 'Fixed', '01-Sep-2026', 'Verified'),

    (12, 3, 'X-Ray', 1, 300.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (13, 3, 'Blood Test', 1, 180.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (14, 3, 'ECG', 1, 200.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (15, 3, 'Health Checkup', 1, 799.0, 'Package', '01-Sep-2026', 'Verified'),

    (16, 4, 'X-Ray', 1, 280.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (17, 4, 'Blood Test', 1, 150.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (18, 4, 'ECG', 1, 180.0, 'Fixed', '01-Sep-2026', 'Verified'),

    (19, 5, 'X-Ray', 1, 450.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (20, 5, 'CT Scan', 1, 1100.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (21, 5, 'MRI', 1, 2300.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (22, 5, 'Health Checkup', 1, 1200.0, 'Package', '01-Sep-2026', 'Verified')
]
cursor.executemany('INSERT INTO services VALUES (?, ?, ?, ?, ?, ?, ?, ?)', services_data)

conn.commit()
conn.close()
print("SUCCESS: Database hospital.db with all tables and data successfully created!")