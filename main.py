# main.py
import time
from monitoring import FileMonitor, monitor_processes, get_system_metrics
from detection import ThreatDetector
from alert_system import send_alert, log_event
from encryption import encrypt_file
from flask import Flask, render_template, redirect, url_for, request, session, flash
from auth_utils import authenticate
from monitoring import FileMonitor
from alert_system import log_event
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-strong-secret-key-here')

# Initialize file monitor
file_monitor = FileMonitor()


@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        with open('system_log.log', 'r') as f:
            logs = f.read()
    except FileNotFoundError:
        logs = "No log file found"

    return render_template('dashboard.html', logs=logs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        error = "Invalid credentials"

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


def run_server():
    file_monitor.start()
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        file_monitor.stop()
    except Exception as e:
        log_event(f"Server error: {str(e)}")
    finally:
        file_monitor.stop()

class RansomwareDefender:
    def __init__(self):
        self.file_monitor = FileMonitor()
        self.detector = ThreatDetector()
        self.running = False

    def start(self):
        """Start monitoring services"""
        self.running = True
        self.file_monitor.start()
        log_event("System started")

        try:
            while self.running:
                self._check_threats()
                time.sleep(5)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            log_event(f"Unexpected error: {str(e)}")
            self.stop()

    def _check_threats(self):
        """Check for ransomware using both models and heuristics"""
        system_metrics = get_system_metrics(self.file_monitor)  # Pass the instance
        if (self.detector.detect(system_metrics) or
                monitor_processes()):
            self._trigger_protection(system_metrics)

    def _trigger_protection(self, metrics):
        """Execute protection measures"""
        send_alert()
        log_event(f"Ransomware detected! Metrics: {metrics}")

        for file_path in self.file_monitor.sensitive_files:
            try:
                encrypt_file(file_path)
                metrics['encryption_calls'] += 1
                log_event(f"Encrypted: {file_path}")
            except Exception as e:
                log_event(f"Encryption failed for {file_path}: {str(e)}")

    def stop(self):
        """Graceful shutdown"""
        self.running = False
        self.file_monitor.stop()
        log_event("System stopped")


if __name__ == "__main__":
    defender = RansomwareDefender()
    defender.start()
    run_server()