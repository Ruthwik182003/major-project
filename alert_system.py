import smtplib
from twilio.rest import Client
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, ALERT_EMAIL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN,TWILIO_PHONE_NUMBER

def send_email_alert():
    try:
        with smtplib.SMTP('smtp.example.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = 'Ransomware Detected!'
            body = 'Ransomware activity has been detected on the system.'
            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(EMAIL_ADDRESS, ALERT_EMAIL, msg)
            print("Email alert sent to administrator.")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def send_sms_alert():
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body="Ransomware detected on the system!",
            from_=TWILIO_PHONE_NUMBER,
            to=ALERT_EMAIL  # Assuming ALERT_EMAIL is a phone number for SMS
        )
        print("SMS alert sent to administrator.")
    except Exception as e:
        print(f"Failed to send SMS alert: {e}")