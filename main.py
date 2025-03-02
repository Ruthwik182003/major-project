import time
from monitoring import FileMonitor, monitor_processes
from detection import detect_ransomware
from alert_system import send_alert
from encryption import encrypt_file
from tagging import tag_sensitive_files

if __name__ == "__main__":
    # Start file system monitoring
    file_monitor = FileMonitor()
    file_monitor.start()

    # Start process monitoring
    try:
        while True:
            if monitor_processes() or detect_ransomware():
                log_event("Ransomware detected!")
                send_alert()
                for file_path in file_monitor.sensitive_files:
                    encrypt_file(file_path)
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        file_monitor.stop()