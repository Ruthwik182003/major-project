from flask import Flask, render_template, redirect, url_for, request, session, flash
from auth_utils import authenticate
from monitoring import FileMonitor
from alert_system import log_event
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# Initialize file monitor
file_monitor = FileMonitor()

@app.route('/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    logs = ""
    if os.path.exists('system_log.log'):
        with open('system_log.log', 'r') as f:
            logs = f.read()
    return render_template('dashboard.html', logs=logs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid credentials. Please try again."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    file_monitor.start()
    app.run(port=5000)