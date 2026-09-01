import mysql.connector

conn = mysql.connector.connect(
    host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    port=4000,
    user="iK3LV5N6M2CshGx.root",
    password="vwlacZZupZDrTZ9d",
    database="test",
    ssl_verify_cert=False
)
cursor = conn.cursor()

# 1. Users Table
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

# 2. Hospitals Table
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

# 3. Services Table
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

# 4. Bookings Table
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
print("All MySQL tables successfully created on TiDB Cloud!")
cursor.close()
conn.close()