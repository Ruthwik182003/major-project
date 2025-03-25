#!/usr/bin/env python3
import time
import psutil
from threading import Thread
from flask import Flask
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config
from config import SECRET_KEY, USERS, SENSITIVE_EXTENSIONS, EMAIL_SETTINGS, LOG_FILE, MODEL_PATHS


# Replace the Config class with direct imports
app = Flask(__name__)
app.secret_key = SECRET_KEY

# When you need configuration:

# ======================
# Core Monitoring System
# ======================
class FileMonitor(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.sensitive_files = set()
        self.observer = Observer()
        self.file_access_count = 0

    def on_modified(self, event):
        if not event.is_directory:
            self.file_access_count += 1
            file_path = event.src_path
            if self._is_sensitive(file_path):
                self.sensitive_files.add(file_path)
                self.log_event(f"Sensitive file modified: {file_path}")

    def _is_sensitive(self, file_path):
        return any(file_path.endswith(ext) for ext in config.SENSITIVE_EXTENSIONS)

    def start(self):
        self.observer.schedule(self, path='.', recursive=True)
        self.observer.start()
        self.log_event("File monitoring started")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        self.log_event("File monitoring stopped")

    def log_event(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(config.LOG_FILE, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")


# ======================
# Threat Detection
# ======================
class ThreatDetector:
    def __init__(self):
        self.model = None  # Load your ML model here
        self.log_event("Threat detector initialized")

    def detect(self, system_metrics):
        # Implement your detection logic
        return False  # Placeholder

    def log_event(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(config.LOG_FILE, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")


# ======================
# Main Application
# ======================
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

file_monitor = FileMonitor()
threat_detector = ThreatDetector()


class RansomwareDefender:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        file_monitor.start()
        self.log_event("Defense system started")

        while self.running:
            self._check_threats()
            time.sleep(5)

    def _check_threats(self):
        if threat_detector.detect(self._get_system_metrics()):
            self._trigger_protection()

    def _get_system_metrics(self):
        return {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'file_access': file_monitor.file_access_count
        }

    def _trigger_protection(self):
        self.log_event("Ransomware detected! Taking protective measures")
        # Implement protection logic here

    def stop(self):
        self.running = False
        file_monitor.stop()
        self.log_event("Defense system stopped")

    def log_event(self, message):
        file_monitor.log_event(message)


# ======================
# Web Interface Routes
# ======================

# app.py
from flask import Flask, render_template, redirect, url_for, request, session, flash
from auth_utils import register_user, authenticate

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Should match config.py


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
        elif register_user(username, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])


# ======================
# Startup Logic
# ======================
def run_defender():
    defender = RansomwareDefender()
    defender.start()


if __name__ == "__main__":
    # Start defender in background thread
    defender_thread = Thread(target=run_defender)
    defender_thread.daemon = True
    defender_thread.start()

    # Start web interface
    app.run(host='0.0.0.0', port=5000, debug=True)