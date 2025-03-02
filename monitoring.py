import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import psutil
from tagging import tag_sensitive_files
from alert_system import log_event

class FileMonitor(FileSystemEventHandler):
    def __init__(self):
        self.sensitive_files = set()
        self.observer = Observer()

    def on_modified(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        if tag_sensitive_files(file_path):
            self.sensitive_files.add(file_path)
            log_event(f"Sensitive file modified: {file_path}")
            print(f"Sensitive file modified: {file_path}")

    def start(self):
        self.observer.schedule(self, path='.', recursive=True)
        self.observer.start()
        log_event("File system monitoring started.")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        log_event("File system monitoring stopped.")

def monitor_processes():
    """
    Monitor system processes for suspicious activity.
    """
    while True:
        suspicious = False
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'io_counters']):
            try:
                cpu_usage = proc.info['cpu_percent']
                io_counters = proc.info['io_counters']
                if cpu_usage > 80 or io_counters.write_bytes > 1e8:  # Example thresholds
                    suspicious = True
                    log_event(f"Suspicious process detected: {proc.info['name']} (PID: {proc.info['pid']})")
                    print(f"Suspicious process detected: {proc.info['name']} (PID: {proc.info['pid']})")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        if suspicious:
            return True  # Ransomware-like behavior detected
        time.sleep(5)  # Check every 5 seconds