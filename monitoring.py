# monitoring.py
import psutil
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from alert_system import log_event


class FileMonitor(FileSystemEventHandler):
    def __init__(self):
        self.sensitive_files = set()
        self.observer = Observer()
        self.file_access_count = 0
        self.api_call_count = 0

    def on_modified(self, event):
        if not event.is_directory:
            self.file_access_count += 1
            file_path = event.src_path
            if tag_sensitive_files(file_path):
                self.sensitive_files.add(file_path)
                log_event(f"Sensitive file modified: {file_path}")

    def start(self):
        self.observer.schedule(self, path='.', recursive=True)
        self.observer.start()
        log_event("File system monitoring started")

    def stop(self):
        self.observer.stop()
        self.observer.join()


def get_system_metrics():
    """Collect all metrics needed by the model"""
    net_io = psutil.net_io_counters()
    disk_io = psutil.disk_io_counters()

    return {
        'cpu_usage': psutil.cpu_percent(),
        'memory_usage': psutil.virtual_memory().percent,
        'file_access': file_monitor.file_access_count,
        'encryption_calls': 0,  # Will be updated during protection
        'network_activity': net_io.bytes_sent + net_io.bytes_recv,
        'suspicious_api_calls': file_monitor.api_call_count,
        'cpu_mem_ratio': psutil.cpu_percent() / max(1, psutil.virtual_memory().percent),
        'encryption_per_file': 0,  # Updated during protection
        'api_per_network': file_monitor.api_call_count / max(1, net_io.bytes_sent + net_io.bytes_recv)
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