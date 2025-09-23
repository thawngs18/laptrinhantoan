from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import time
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Store OTP in memory (for demo purposes)
otp_storage = {}

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def is_valid_phone(phone):
    """Validate Vietnamese phone number"""
    if len(phone) != 10 or not phone.startswith('0'):
        return False
    # Check for valid mobile prefixes
    valid_prefixes = ['03', '05', '07', '08', '09']
    prefix = phone[:2]
    return prefix in valid_prefixes

def user_exists(phone):
    """Check if user already exists"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM users WHERE phone = ?', (phone,))
    result = cursor.fetchone()
    conn.close()
    return result

def register_user(name, phone):
    """Register new user"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, phone) VALUES (?, ?)', (name, phone))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# New registration route
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        # Validation
        if not name or len(name) < 2:
            return jsonify({
                'success': False,
                'message': 'Tên không hợp lệ (ít nhất 2 ký tự)'
            }), 400
        
        if not phone or not is_valid_phone(phone):
            return jsonify({
                'success': False,
                'message': 'Số điện thoại không hợp lệ'
            }), 400
        
        # Check if user already exists
        if user_exists(phone):
            return jsonify({
                'success': False,
                'message': 'Số điện thoại này đã được đăng ký'
            }), 400
        
        # Register new user
        if register_user(name, phone):
            return jsonify({
                'success': True,
                'message': 'Đăng ký thành công',
                'name': name,
                'phone': phone
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Lỗi khi đăng ký. Vui lòng thử lại.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()
        
        # Check if user is registered
        user = user_exists(phone)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Số điện thoại này chưa được đăng ký. Vui lòng đăng ký trước.'
            }), 400
        
        if not phone or not is_valid_phone(phone):
            return jsonify({
                'success': False,
                'message': 'Số điện thoại không hợp lệ'
            }), 400
        
        # Generate and store OTP (valid for 5 minutes)
        otp = generate_otp()
        otp_storage[phone] = {
            'otp': otp,
            'expires': time.time() + 300,  # 5 minutes
            'name': user[1]  # Store user name
        }
        
        # In production, you would send SMS here
        print(f"OTP for {phone}: {otp}")  # For demo purposes
        
        return jsonify({
            'success': True,
            'message': 'OTP đã được gửi thành công',
            'phone': phone
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        phone = data.get('phone', '').strip()
        otp = data.get('otp', '').strip()
        
        # Check if user is registered
        user = user_exists(phone)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Số điện thoại này chưa được đăng ký'
            }), 400
        
        if not phone or not otp:
            return jsonify({
                'success': False,
                'message': 'Thiếu thông tin số điện thoại hoặc mã OTP'
            }), 400
        
        if phone not in otp_storage:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy mã OTP cho số điện thoại này'
            }), 400
        
        stored_data = otp_storage[phone]
        
        # Check if OTP expired
        if time.time() > stored_data['expires']:
            del otp_storage[phone]
            return jsonify({
                'success': False,
                'message': 'Mã OTP đã hết hạn'
            }), 400
        
        # Verify OTP
        if otp != stored_data['otp']:
            return jsonify({
                'success': False,
                'message': 'Mã OTP không đúng'
            }), 400
        
        # Success - clean up storage
        del otp_storage[phone]
        
        return jsonify({
            'success': True,
            'message': 'Xác thực thành công',
            'name': stored_data['name'],
            'phone': phone
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Lỗi server: {str(e)}'
        }), 500

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == "__main__":
    # Initialize database
    init_db()
    app.run(debug=True)