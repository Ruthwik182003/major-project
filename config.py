# config.py (
import os
from werkzeug.security import generate_password_hash

# User storage (consider using a database in production)
USER_DB = 'users.db'  # File to store user credentials
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize user storage if it doesn't exist
if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        # Default admin user
        default_users = {
            "admin": generate_password_hash("admin123")
        }
        f.write(str(default_users))

# Model paths (if you're using ML)
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATHS = {
    'model': 'models/best_ransomware_model.pkl',
    'scaler': 'models/ransomware_scaler.pkl'
}

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
USERS = {
    "admin": generate_password_hash("admin_password")  # Auto-hashes the password
}

# File monitoring
SENSITIVE_EXTENSIONS = ['.docx', '.pdf', '.xls', '.xlsx', '.txt', '.csv']
SENSITIVE_KEYWORDS = ['confidential', 'secret', 'password']

# Email alerts
EMAIL_SETTINGS = {
    'address': 'anjananju2715@gmail.com',
    'password': 'your-email-password',  # Consider using app-specific password
    'recipient': 'anjananju2715@gmail.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# System paths
LOG_FILE = 'system_log.log'
BACKUP_DIR = 'backups'
ENCRYPTION_KEY_PATH = 'encryption_key.key'