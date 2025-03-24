# alert_system.py
import smtplib
from email.mime.text import MIMEText
import time
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, ALERT_EMAIL, LOG_FILE


def send_alert(subject="Ransomware Detected!", body=None):
    """Send email alert with detailed metrics"""
    if body is None:
        body = "Suspicious activity detected by the ransomware protection system."

    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = ALERT_EMAIL

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        log_event("Alert email sent successfully")
    except Exception as e:
        log_event(f"Failed to send alert: {str(e)}")


def log_event(message):
    """Log system events with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"

    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_line)
    except IOError:
        print(f"Failed to write to log: {log_line}")