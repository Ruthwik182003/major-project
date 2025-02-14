import shutil
import os
from datetime import datetime
from config import BACKUP_DIR

def backup_files(file_paths):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)
    for file_path in file_paths:
        shutil.copy(file_path, backup_path)
    print(f"Backup created at: {backup_path}")