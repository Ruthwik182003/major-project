import psutil
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from alert_system import log_event
from threading import Lock

# Define this function before the class that uses it
def tag_sensitive_files(file_path):
    """Determine if a file is sensitive based on its content/extension"""
    # Your implementation here
    # Example:
    sensitive_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.txt']
    return any(file_path.lower().endswith(ext) for ext in sensitive_extensions)

class FileMonitor(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.sensitive_files = set()
        self.observer = Observer()
        self.file_access_count = 0
        self.api_call_count = 0
        self.running = False
        self.lock = Lock()

    def on_modified(self, event):
        if not event.is_directory and self.running:
            with self.lock:
                self.file_access_count += 1
                file_path = event.src_path
                if tag_sensitive_files(file_path):
                    self.sensitive_files.add(file_path)
                    log_event(f"Sensitive file modified: {file_path}")

    def start(self):
        if not self.running:
            self.observer.schedule(self, path='.', recursive=True)
            self.observer.start()
            self.running = True
            log_event("File system monitoring started")

    def stop(self):
        if self.running:
            self.observer.stop()
            self.observer.join()
            self.running = False

def get_system_metrics(file_monitor_instance):
    """Collect all metrics needed by the model"""
    net_io = psutil.net_io_counters()
    disk_io = psutil.disk_io_counters()

    return {
        'cpu_usage': psutil.cpu_percent(),
        'memory_usage': psutil.virtual_memory().percent,
        'file_access': file_monitor_instance.file_access_count,
        'encryption_calls': 0,
        'network_activity': net_io.bytes_sent + net_io.bytes_recv,
        'suspicious_api_calls': file_monitor_instance.api_call_count,
        'cpu_mem_ratio': psutil.cpu_percent() / max(1, psutil.virtual_memory().percent),
        'encryption_per_file': 0,
        'api_per_network': file_monitor_instance.api_call_count / max(1, net_io.bytes_sent + net_io.bytes_recv)
    }

def monitor_processes():
    """Check for suspicious process behavior"""
    suspicious = False
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            if proc.info['cpu_percent'] > 80 and proc.info['memory_percent'] > 70:
                suspicious = True
                log_event(f"Suspicious process: {proc.info['name']}")
                break
        except psutil.NoSuchProcess:
            continue
    return suspicious