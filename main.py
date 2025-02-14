import time
from monitoring import FileMonitor, monitor_processes
from detection import detect_ransomware
from alert_system import send_email_alert, send_sms_alert
from encryption import encrypt_file
from tagging import tag_sensitive_files
from logging_utils import log_event
from backup_utils import backup_files
from forensic_utils import forensic_analysis
from threat_intel_utils import check_virustotal
from integrity_utils import calculate_file_hash

if __name__ == "__main__":
    # Start file system monitoring
    file_monitor = FileMonitor()
    file_monitor.start()

    # Start process monitoring
    try:
        while True:
            if detect_ransomware():
                log_event("Ransomware detected!")
                send_email_alert()
                send_sms_alert()
                for file_path in file_monitor.sensitive_files:
                    encrypt_file(file_path)
                backup_files(file_monitor.sensitive_files)
                forensic_analysis()
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        file_monitor.stop()