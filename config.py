# config.py
MODEL_PATHS = {
    'scaler': 'ransomware_scaler.pkl',
    'model': 'ransomware_detection_model.pkl',
    'metadata': 'model_metadata.pkl'
}

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