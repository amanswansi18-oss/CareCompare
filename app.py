import os
import math
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'carecompare_secret_key_2026'

# Database Configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com'),
    'port': int(os.environ.get('DB_PORT', 4000)),
    'user': os.environ.get('DB_USER', 'iK3LV5N6M2CshGx.root'),
    'password': os.environ.get('DB_PASSWORD', 'vwlacZZupZDrTZ9d'),
    'database': os.environ.get('DB_NAME', 'test'),
    'ssl_verify_cert': False
}
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def calculate_distance(lat1, lon1, lat2, lon2):
    if not lat1 or not lon1 or not lat2 or not lon2:
        return 9999.0
    R = 6371.0  # Earth radius in KM
    dlat = math.radians(float(lat2) - float(lat1))
    dlon = math.radians(float(lon2) - float(lon1))
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

# ----------------- HOME ROUTE -----------------
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT h.hospital_id, h.hospital_name, h.area, h.city, h.rating, h.image_url, 
               MIN(s.price_inr) as starting_price
        FROM hospitals h
        LEFT JOIN services s ON h.hospital_id = s.hospital_id
        GROUP BY h.hospital_id, h.hospital_name, h.area, h.city, h.rating, h.image_url
        ORDER BY h.rating DESC
        LIMIT 6
    ''')
    top_hospitals = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', top_hospitals=top_hospitals)

# ----------------- SEARCH ROUTE -----------------
@app.route('/search', methods=['GET'])
def search():
    service_query = request.args.get('service', '').strip()
    location_query = request.args.get('location', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    clean_service = service_query.replace('-', '').replace(' ', '').lower()

    sql = '''
        SELECT h.hospital_id, h.hospital_name, h.area, h.city, h.rating, h.phone, h.doctors_count, h.image_url,
               s.service_id, s.service_name, MIN(s.price_inr) AS price_inr, s.verification_status, s.last_updated
        FROM hospitals h
        JOIN services s ON h.hospital_id = s.hospital_id
        WHERE (
            LOWER(REPLACE(REPLACE(s.service_name, '-', ''), ' ', '')) LIKE %s
            OR LOWER(s.service_name) LIKE %s
        )
    '''
    params = [f'%{clean_service}%', f'%{service_query.lower()}%']

    if location_query:
        parts = [p.strip() for p in location_query.split(',') if p.strip()]
        loc_clauses = []
        for part in parts:
            loc_clauses.append('(LOWER(h.city) LIKE %s OR LOWER(h.area) LIKE %s OR LOWER(h.state) LIKE %s)')
            params.extend([f'%{part.lower()}%', f'%{part.lower()}%', f'%{part.lower()}%'])
        
        if loc_clauses:
            sql += ' AND (' + ' OR '.join(loc_clauses) + ')'

    sql += ' GROUP BY h.hospital_id, h.hospital_name, h.area, h.city, h.rating, h.phone, h.doctors_count, h.image_url, s.service_id, s.service_name, s.verification_status, s.last_updated'
    sql += ' ORDER BY price_inr ASC'

    cursor.execute(sql, tuple(params))
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('hospitals.html', results=results, query=service_query, location=location_query)

# ----------------- NEARBY (LIVE LOCATION) ROUTE -----------------
@app.route('/nearby')
def nearby():
    user_lat = request.args.get('lat', type=float)
    user_lon = request.args.get('lon', type=float)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('''
        SELECT h.hospital_id, h.hospital_name, h.area, h.city, h.rating, h.phone, 
               h.doctors_count, h.image_url, h.latitude, h.longitude,
               MIN(s.price_inr) as starting_price
        FROM hospitals h
        LEFT JOIN services s ON h.hospital_id = s.hospital_id
        GROUP BY h.hospital_id, h.hospital_name, h.area, h.city, h.rating, h.phone, h.doctors_count, h.image_url, h.latitude, h.longitude
    ''')
    hospitals = cursor.fetchall()
    cursor.close()
    conn.close()

    for h in hospitals:
        if user_lat and user_lon and h.get('latitude') and h.get('longitude'):
            h['distance_km'] = calculate_distance(user_lat, user_lon, h['latitude'], h['longitude'])
        else:
            h['distance_km'] = 'N/A'

    if user_lat and user_lon:
        hospitals.sort(key=lambda x: x['distance_km'] if isinstance(x['distance_km'], (int, float)) else 9999)

    return render_template('nearby.html', hospitals=hospitals, user_lat=user_lat, user_lon=user_lon)

# ----------------- HOSPITAL DETAILS ROUTE -----------------
@app.route('/hospital/<int:hospital_id>')
def hospital_details(hospital_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM hospitals WHERE hospital_id = %s', (hospital_id,))
    hospital = cursor.fetchone()
    
    cursor.execute('SELECT * FROM services WHERE hospital_id = %s ORDER BY price_inr ASC', (hospital_id,))
    services = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not hospital:
        return "Hospital not found", 404
        
    return render_template('hospital_details.html', hospital=hospital, services=services)

# ----------------- AUTHENTICATION: REGISTER -----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            flash('Email already registered! Kripya login karein.', 'warning')
            cursor.close()
            conn.close()
            return redirect(url_for('login'))

        cursor.execute('''
            INSERT INTO users (full_name, email, phone, password, created_at)
            VALUES (%s, %s, %s, %s, NOW())
        ''', (full_name, email, phone, password))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Account successfully create ho gaya! Ab login karein.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# ----------------- AUTHENTICATION: LOGIN -----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['user_id']
            session['user_name'] = user['full_name']
            session['user_email'] = user['email']
            flash(f"Welcome back, {user['full_name']}!", 'success')
            return redirect(url_for('home'))
        else:
            flash('Galat email ya password. Kripya dobara try karein.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# ----------------- LOGOUT -----------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Aap successfully logout ho chuke hain.', 'info')
    return redirect(url_for('home'))

# ----------------- BOOKING & DASHBOARD -----------------
@app.route('/book/<int:service_id>', methods=['GET', 'POST'])
def book(service_id):
    if 'user_id' not in session:
        flash('Booking karne ke liye pehle login karein.', 'warning')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        patient_phone = request.form.get('patient_phone')
        appointment_date = request.form.get('appointment_date')
        notes = request.form.get('notes', '')

        cursor.execute('''
            INSERT INTO bookings (user_id, service_id, patient_name, patient_phone, appointment_date, notes, status, booking_time)
            VALUES (%s, %s, %s, %s, %s, %s, 'Confirmed', NOW())
        ''', (session['user_id'], service_id, patient_name, patient_phone, appointment_date, notes))
        conn.commit()
        booking_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return redirect(url_for('booking_success', booking_id=booking_id))

    cursor.execute('''
        SELECT s.*, h.hospital_name, h.area, h.city 
        FROM services s
        JOIN hospitals h ON s.hospital_id = h.hospital_id
        WHERE s.service_id = %s
    ''', (service_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('book.html', item=item)

@app.route('/booking-success/<int:booking_id>')
def booking_success(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT b.*, s.service_name, s.price_inr, h.hospital_name, h.area, h.city, h.phone as hospital_phone
        FROM bookings b
        JOIN services s ON b.service_id = s.service_id
        JOIN hospitals h ON s.hospital_id = h.hospital_id
        WHERE b.booking_id = %s
    ''', (booking_id,))
    booking = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('booking_success.html', booking=booking)

@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT b.*, s.service_name, s.price_inr, h.hospital_name, h.area, h.city
        FROM bookings b
        JOIN services s ON b.service_id = s.service_id
        JOIN hospitals h ON s.hospital_id = h.hospital_id
        WHERE b.user_id = %s
        ORDER BY b.booking_id DESC
    ''', (session['user_id'],))
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('my_bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True, port=5000)