# app/main.py

import os
import threading
from flask import (
    request, render_template, redirect,
    url_for, session, flash, jsonify
)
from werkzeug.utils import secure_filename

from . import create_app, db
from .models import User
from .file_io import read_file
from .processing import process_file_pipeline
from .fs_monitor import start_monitor, LOGS

# Create Flask app & initialize database
app = create_app()
with app.app_context():
    db.create_all()

# Directory to store uploads
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Start filesystem monitor in background
threading.Thread(target=start_monitor, args=(UPLOAD_DIR,), daemon=True).start()

# Tag → Category mapping (normalized keys: no spaces or hyphens)
CATEGORIES = {
    '#array':         'Arrays and Hashing',
    '#twopointers':   'Two Pointers',
    '#slidingwindow': 'Sliding Window',
    '#stack':         'Stack',
    '#binarysearch':  'Binary Search',
    '#linkedlist':    'Linked List',
    '#trees':         'Trees',
    '#heap':          'Heap',
    '#backtracking':  'BackTracking',
    '#tries':         'Tries',
    '#graphs':        'Graphs',
    '#dp':            'DP',
    '#greedy':        'Greedy'
}

# ─── Registration ───────────────────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username'].strip()
        pwd = request.form['password'].strip()
        if not uname or not pwd:
            flash("Username & password required", "warning")
            return redirect(url_for('register'))
        if User.query.filter_by(username=uname).first():
            flash("Username already taken", "danger")
            return redirect(url_for('register'))
        user = User(username=uname)
        user.set_password(pwd)
        db.session.add(user)
        db.session.commit()
        flash("Registered! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

# ─── Login / Logout ────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username'].strip()
        pwd = request.form['password'].strip()
        user = User.query.filter_by(username=uname).first()
        if user and user.check_password(pwd):
            session['user'] = uname
            flash("Logged in successfully", "success")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─── Dashboard & Upload ─────────────────────────────────────────────────

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Handle file upload
    if request.method == 'POST':
        f = request.files.get('file')
        if not f:
            flash("No file selected", "warning")
            return redirect(url_for('dashboard'))
        filename = secure_filename(f.filename)
        save_path = os.path.join(UPLOAD_DIR, filename)
        f.save(save_path)
        process_file_pipeline(filename)
        flash("File uploaded & processed", "success")
        return redirect(url_for('dashboard'))

    # Compute counts per category, skip .summary.txt files
    counts = {cat: 0 for cat in set(CATEGORIES.values()) | {'Miscellaneous'}}
    for fn in os.listdir(UPLOAD_DIR):
        if fn.endswith('.summary.txt'):
            continue
        lines = read_file(os.path.join(UPLOAD_DIR, fn))
        cat = 'Miscellaneous'
        for ln in lines:
            norm = ln.lower().replace(' ', '').replace('-', '')
            for tag, name in CATEGORIES.items():
                if tag in norm:
                    cat = name
                    break
            if cat != 'Miscellaneous':
                break
        counts[cat] += 1

    return render_template('dashboard.html', counts=counts)

# ─── Category Detail Page ───────────────────────────────────────────────

@app.route('/category/<category>')
def show_category(category):
    if 'user' not in session:
        return redirect(url_for('login'))

    entries = []
    for entry in reversed(LOGS):
        fn = entry['file']
        if fn.endswith('.summary.txt'):
            continue
        lines = read_file(os.path.join(UPLOAD_DIR, fn))
        cat = 'Miscellaneous'
        for ln in lines:
            norm = ln.lower().replace(' ', '').replace('-', '')
            for tag, name in CATEGORIES.items():
                if tag in norm:
                    cat = name
                    break
            if cat != 'Miscellaneous':
                break
        if cat == category:
            entries.append(entry)

    return render_template('category.html', category=category, entries=entries)
