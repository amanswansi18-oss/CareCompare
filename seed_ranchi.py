import mysql.connector

# Database Connection (TiDB Cloud)
conn = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="iK3LV5N6M2CshGx.root",
    password="vwlacZZupZDrTZ9d",
    database="test",
    ssl_verify_cert=False
)
cursor = conn.cursor()

# 1. Pehle saari tables banao agar nahi hain
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    city VARCHAR(50)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_name VARCHAR(150) NOT NULL,
    address TEXT,
    city VARCHAR(50),
    latitude DOUBLE,
    longitude DOUBLE,
    contact_number VARCHAR(50),
    rating FLOAT DEFAULT 4.0,
    image_url TEXT,
    doctors_count INT DEFAULT 10,
    beds_count INT DEFAULT 50,
    icu_beds_count INT DEFAULT 10,
    emergency_available VARCHAR(10) DEFAULT 'Yes'
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    hospital_id INT NOT NULL,
    service_name VARCHAR(100) NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id) ON DELETE CASCADE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    hospital_id INT NOT NULL,
    service_id INT,
    patient_name VARCHAR(100),
    patient_phone VARCHAR(20),
    appointment_date VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id) ON DELETE CASCADE
);
""")
conn.commit()

# 2. Safely Clear Existing Data
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
cursor.execute("TRUNCATE TABLE services;")
cursor.execute("TRUNCATE TABLE hospitals;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
conn.commit()

# 3. Ranchi Hospitals Data Insert
hospitals_data = [
    ("Rajendra Institute of Medical Sciences (RIMS)", "Bariatu, Ranchi, Jharkhand 834009", "Ranchi", 23.3888, 85.3587, "+91 651 2541533", 4.3, "https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?auto=format&fit=crop&w=600&q=80", 120, 1500, 120, "Yes"),
    ("Medanta Hospital Ranchi", "P.O. Irba, NH 33, Ranchi, Jharkhand 835217", "Ranchi", 23.4754, 85.4526, "+91 651 7123100", 4.6, "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=600&q=80", 65, 450, 60, "Yes"),
    ("Paras HEC Hospital", "Dhurwa, Sector 2, Ranchi, Jharkhand 834004", "Ranchi", 23.3102, 85.2981, "+91 651 7100100", 4.5, "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=600&q=80", 50, 300, 45, "Yes"),
    ("Bhagwan Mahavir Medica Superspecialty", "Bariatu Road, Ranchi, Jharkhand 834009", "Ranchi", 23.3912, 85.3615, "+91 651 6606000", 4.4, "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=600&q=80", 55, 300, 50, "Yes"),
    ("Sadar Hospital Ranchi", "Purulia Road, Ranchi, Jharkhand 834001", "Ranchi", 23.3694, 85.3342, "+91 651 2212345", 4.1, "https://images.unsplash.com/photo-1538108149393-fbbd81895907?auto=format&fit=crop&w=600&q=80", 40, 500, 30, "Yes"),
    ("Orchid Medical Centre", "HB Road, Lalpur, Ranchi, Jharkhand 834001", "Ranchi", 23.3658, 85.3412, "+91 651 7100000", 4.3, "https://images.unsplash.com/photo-1512678080530-7760d81faba6?auto=format&fit=crop&w=600&q=80", 35, 150, 25, "Yes")
]

h_query = """
INSERT INTO hospitals (hospital_name, address, city, latitude, longitude, contact_number, rating, image_url, doctors_count, beds_count, icu_beds_count, emergency_available)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(h_query, hospitals_data)
conn.commit()

# Hospital IDs map karein
cursor.execute("SELECT hospital_id, hospital_name FROM hospitals")
hosp_rows = cursor.fetchall()
hosp_map = {row[1]: row[0] for row in hosp_rows}

# 4. Services Data Insert
services_data = [
    (hosp_map["Rajendra Institute of Medical Sciences (RIMS)"], "General OPD Consultation", 50.00, "Consultation"),
    (hosp_map["Rajendra Institute of Medical Sciences (RIMS)"], "ICU Charges (Per Day)", 1200.00, "Inpatient"),
    (hosp_map["Rajendra Institute of Medical Sciences (RIMS)"], "MRI Brain Scan", 2500.00, "Diagnostic"),
    (hosp_map["Rajendra Institute of Medical Sciences (RIMS)"], "CT Scan Whole Abdomen", 1800.00, "Diagnostic"),
    
    (hosp_map["Medanta Hospital Ranchi"], "General OPD Consultation", 800.00, "Consultation"),
    (hosp_map["Medanta Hospital Ranchi"], "ICU Charges (Per Day)", 7500.00, "Inpatient"),
    (hosp_map["Medanta Hospital Ranchi"], "MRI Brain Scan", 7000.00, "Diagnostic"),
    (hosp_map["Medanta Hospital Ranchi"], "CT Scan Whole Abdomen", 5500.00, "Diagnostic"),

    (hosp_map["Paras HEC Hospital"], "General OPD Consultation", 600.00, "Consultation"),
    (hosp_map["Paras HEC Hospital"], "ICU Charges (Per Day)", 5500.00, "Inpatient"),
    (hosp_map["Paras HEC Hospital"], "MRI Brain Scan", 6000.00, "Diagnostic"),

    (hosp_map["Bhagwan Mahavir Medica Superspecialty"], "General OPD Consultation", 700.00, "Consultation"),
    (hosp_map["Bhagwan Mahavir Medica Superspecialty"], "ICU Charges (Per Day)", 6000.00, "Inpatient"),

    (hosp_map["Sadar Hospital Ranchi"], "General OPD Consultation", 20.00, "Consultation"),
    (hosp_map["Sadar Hospital Ranchi"], "ICU Charges (Per Day)", 800.00, "Inpatient"),

    (hosp_map["Orchid Medical Centre"], "General OPD Consultation", 650.00, "Consultation"),
    (hosp_map["Orchid Medical Centre"], "ICU Charges (Per Day)", 5000.00, "Inpatient")
]

s_query = "INSERT INTO services (hospital_id, service_name, cost, category) VALUES (%s, %s, %s, %s)"
cursor.executemany(s_query, services_data)
conn.commit()

print("Tables Created & Ranchi Hospitals Data Successfully Inserted into TiDB!")
cursor.close()
conn.close()