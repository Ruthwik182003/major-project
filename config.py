# config.py
import os

# Model paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATHS = {
    'model': 'models/best_ransomware_model.pkl',  # Updated to existing file
    'scaler': 'models/ransomware_scaler.pkl',
    'metadata': 'models/model_metadata.pkl'
}

# Rest of your config remains the same...

# Rest of your existing config...
SENSITIVE_ENTITIES = ["PERSON", "ORG", "GPE", "EMAIL", "CARD_NUMBER"]
SENSITIVE_EXTENSIONS = ['.docx', '.pdf', '.xls', '.xlsx', '.txt', '.csv']
SENSITIVE_KEYWORDS = ['confidential', 'secret', 'password', 'ssn', 'credit card']
ENCRYPTION_KEY_PATH = 'encryption_key.key'
LOG_FILE = 'system_log.log'
BACKUP_DIR = 'backups'
EMAIL_ADDRESS = 'anjananju2715@gmail.com'
EMAIL_PASSWORD = 'anju2713'
ALERT_EMAIL = 'anjananju2715@gmail.com'
SECRET_KEY = 'your_secret_key'