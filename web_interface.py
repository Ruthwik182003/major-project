from flask import Flask, render_template
import threading
from main import file_monitor
from auth_utils import auth

app = Flask(__name__)

@app.route('/')
@auth.login_required
def dashboard():
    status = "Monitoring..." if file_monitor.observer.is_alive() else "Stopped"
    alerts = "No alerts" if not file_monitor.sensitive_files else "Ransomware detected!"
    return render_template('dashboard.html', status=status, alerts=alerts)

def run_web_interface():
    app.run(port=5000)

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_interface)
    web_thread.start()