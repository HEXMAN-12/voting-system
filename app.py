from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import hashlib
from datetime import datetime
import os
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database setup
def init_db():
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            cnic TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            has_voted BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Votes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            party TEXT NOT NULL,
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Party statistics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS party_stats (
            party TEXT PRIMARY KEY,
            vote_count INTEGER DEFAULT 0
        )
    ''')
    
    # Initialize party stats
    parties = ['PMLN', 'PTI', 'ARMY']
    for party in parties:
        cursor.execute('INSERT OR IGNORE INTO party_stats (party, vote_count) VALUES (?, 0)', (party,))
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_cnic(cnic):
    # Pakistani CNIC format: 12345-1234567-1
    pattern = r'^\d{5}-\d{7}-\d{1}$'
    return re.match(pattern, cnic) is not None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('vote'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cnic = data.get('cnic', '').strip()
    password = data.get('password', '')
    
    if not cnic or not password:
        return jsonify({'success': False, 'message': 'Please fill in all fields'})
    
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, first_name, last_name, password_hash, has_voted FROM users WHERE cnic = ?', (cnic,))
    user = cursor.fetchone()
    
    if user and user[3] == hash_password(password):
        session['user_id'] = user[0]
        session['user_name'] = f"{user[1]} {user[2]}"
        session['has_voted'] = user[4]
        conn.close()
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        conn.close()
        return jsonify({'success': False, 'message': 'Invalid CNIC or password'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    required_fields = ['first_name', 'last_name', 'cnic', 'email', 'phone', 'address', 'password']
    for field in required_fields:
        if not data.get(field, '').strip():
            return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'})
    
    first_name = data['first_name'].strip()
    last_name = data['last_name'].strip()
    cnic = data['cnic'].strip()
    email = data['email'].strip().lower()
    phone = data['phone'].strip()
    address = data['address'].strip()
    password = data['password']
    
    # Validate CNIC format
    if not validate_cnic(cnic):
        return jsonify({'success': False, 'message': 'Invalid CNIC format. Use: 12345-1234567-1'})
    
    # Validate email format
    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Invalid email format'})
    
    # Validate password length
    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters long'})
    
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE cnic = ? OR email = ?', (cnic, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'message': 'User with this CNIC or email already exists'})
        
        # Insert new user
        cursor.execute('''
            INSERT INTO users (first_name, last_name, cnic, email, phone, address, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, cnic, email, phone, address, hash_password(password)))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
        
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'User with this CNIC or email already exists'})

@app.route('/vote')
def vote():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    return render_template('vote.html', 
                         user_name=session.get('user_name'), 
                         has_voted=session.get('has_voted'))

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login first'})
    
    if session.get('has_voted'):
        return jsonify({'success': False, 'message': 'You have already voted'})
    
    data = request.get_json()
    party = data.get('party')
    
    if party not in ['PMLN', 'PTI', 'ARMY']:
        return jsonify({'success': False, 'message': 'Invalid party selection'})
    
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    
    try:
        # Record the vote
        cursor.execute('INSERT INTO votes (user_id, party) VALUES (?, ?)', 
                      (session['user_id'], party))
        
        # Update user's voting status
        cursor.execute('UPDATE users SET has_voted = TRUE WHERE id = ?', 
                      (session['user_id'],))
        
        # Update party statistics
        cursor.execute('UPDATE party_stats SET vote_count = vote_count + 1 WHERE party = ?', 
                      (party,))
        
        conn.commit()
        session['has_voted'] = True
        
        conn.close()
        return jsonify({'success': True, 'message': f'Your vote for {party} has been registered!'})
        
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': 'An error occurred while casting your vote'})

@app.route('/results')
def results():
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT party, vote_count FROM party_stats ORDER BY vote_count DESC')
    results = cursor.fetchall()
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE has_voted = TRUE')
    total_votes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('results.html', 
                         results=results, 
                         total_votes=total_votes,
                         total_users=total_users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    # Simple admin page to view all data
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    
    # Get all users
    cursor.execute('''
        SELECT u.first_name, u.last_name, u.cnic, u.email, u.has_voted, v.party, v.voted_at
        FROM users u
        LEFT JOIN votes v ON u.id = v.user_id
        ORDER BY u.created_at DESC
    ''')
    users = cursor.fetchall()
    
    # Get party statistics
    cursor.execute('SELECT party, vote_count FROM party_stats ORDER BY vote_count DESC')
    stats = cursor.fetchall()
    
    # Count voted users
    cursor.execute('SELECT COUNT(*) FROM users WHERE has_voted = TRUE')
    voted_users_count = cursor.fetchone()[0]
    
    # Count total users
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template('admin.html', 
                         users=users, 
                         stats=stats,
                         voted_users_count=voted_users_count,
                         total_users_count=total_users_count)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
