
import mysql.connector

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aman123",  # <--- Apna MySQL password daalein
    database="carecompare_db"
)
cursor = conn.cursor()

# 1. Missing columns ko safely add karein agar nahi hain
try:
    cursor.execute("ALTER TABLE hospitals ADD COLUMN image_url VARCHAR(500);")
except Exception:
    pass

try:
    cursor.execute("ALTER TABLE hospitals ADD COLUMN doctors_count INT DEFAULT 20;")
except Exception:
    pass

try:
    cursor.execute("ALTER TABLE hospitals ADD COLUMN beds INT DEFAULT 100;")
except Exception:
    pass

# 2. Foreign keys off karke purana data clean karein
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("TRUNCATE TABLE services;")
cursor.execute("TRUNCATE TABLE hospitals;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

# 3. Ranchi Hospitals Insert (Bina 'address' column ke exact schema match)
hospitals_data = [
    (1, 'RIMS (Rajendra Institute of Medical Sciences)', 'Bariatu', 'Ranchi', 'Jharkhand', '834009', '06512541533', 4.5, 120, 1500, 'Govt Verified', 23.3882, 85.3575, 'https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?w=800&q=80'),
    (2, 'Bhagwan Mahavir Medica Hospital', 'Bariatu', 'Ranchi', 'Jharkhand', '834009', '06516606000', 4.8, 65, 300, 'Verified', 23.3934, 85.3610, 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&q=80'),
    (3, 'Medanta Hospital Ranchi', 'Booty More', 'Ranchi', 'Jharkhand', '835238', '06516607777', 4.7, 85, 450, 'Verified', 23.4475, 85.4520, 'https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800&q=80'),
    (4, 'Orchid Medical Centre', 'Lalpur', 'Ranchi', 'Jharkhand', '834001', '06516605000', 4.6, 50, 150, 'Verified', 23.3685, 85.3340, 'https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80'),
    (5, 'Raj Hospital', 'Main Road', 'Ranchi', 'Jharkhand', '834001', '06512331763', 4.4, 40, 120, 'Verified', 23.3512, 85.3245, 'https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=800&q=80'),
    (6, 'Sadar Hospital Ranchi', 'Purulia Road', 'Ranchi', 'Jharkhand', '834001', '06512330400', 4.3, 45, 200, 'Govt Verified', 23.3640, 85.3315, 'https://images.unsplash.com/photo-1512678080530-7760d81faba6?w=800&q=80')
]

cursor.executemany('''
    INSERT INTO hospitals (hospital_id, hospital_name, area, city, state, pincode, phone, rating, doctors_count, beds, verification_status, latitude, longitude, image_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
''', hospitals_data)

# 4. Ranchi Diagnostic Rates Insert
services_data = [
    # RIMS
    (1, 'X-Ray', 1, 100.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (1, 'Blood Test', 1, 80.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (1, 'CT Scan', 1, 1200.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (1, 'MRI Scan', 1, 2500.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (1, 'Health Checkup', 1, 499.0, 'Package', '01-Sep-2026', 'Verified'),
    # Medica
    (2, 'X-Ray', 1, 450.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (2, 'Blood Test', 1, 350.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (2, 'CT Scan', 1, 3200.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (2, 'MRI Scan', 1, 6500.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (2, 'Health Checkup', 1, 1499.0, 'Package', '01-Sep-2026', 'Verified'),
    # Medanta
    (3, 'X-Ray', 1, 500.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (3, 'Blood Test', 1, 400.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (3, 'CT Scan', 1, 3500.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (3, 'MRI Scan', 1, 7000.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (3, 'Health Checkup', 1, 1999.0, 'Package', '01-Sep-2026', 'Verified'),
    # Orchid
    (4, 'X-Ray', 1, 350.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (4, 'Blood Test', 1, 250.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (4, 'CT Scan', 1, 2800.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (4, 'MRI Scan', 1, 5500.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (4, 'Health Checkup', 1, 999.0, 'Package', '01-Sep-2026', 'Verified'),
    # Raj Hospital
    (5, 'X-Ray', 1, 300.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (5, 'Blood Test', 1, 200.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (5, 'CT Scan', 1, 2600.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (5, 'MRI Scan', 1, 5000.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (5, 'Health Checkup', 1, 899.0, 'Package', '01-Sep-2026', 'Verified'),
    # Sadar Hospital
    (6, 'X-Ray', 1, 150.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (6, 'Blood Test', 1, 100.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (6, 'CT Scan', 1, 1500.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (6, 'MRI Scan', 1, 3000.0, 'Fixed', '01-Sep-2026', 'Verified'),
    (6, 'Health Checkup', 1, 599.0, 'Package', '01-Sep-2026', 'Verified')
]

cursor.executemany('''
    INSERT INTO services (hospital_id, service_name, available, price_inr, price_type, last_updated, verification_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
''', services_data)

conn.commit()
cursor.close()
conn.close()
print("SUCCESS: Ranchi Hospitals aur Services Database mein successfully load ho gaye!")