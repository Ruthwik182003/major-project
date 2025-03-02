import smtplib
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, ALERT_EMAIL, LOG_FILE

def send_alert():
    """
    Send an email alert to the administrator.
    """
    try:
        with smtplib.SMTP('smtp.example.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = 'Ransomware Detected!'
            body = 'Ransomware activity has been detected on the system.'
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(EMAIL_ADDRESS, ALERT_EMAIL, msg)
            log_event("Email alert sent to administrator.")
    except Exception as e:
        log_event(f"Failed to send email alert: {e}")

def log_event(message):
    """
    Log system events to a file.
    """
    with open(LOG_FILE, 'a') as f:
        f.write(f"{time.ctime()} - {message}\n")