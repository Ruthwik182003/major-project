#!/usr/bin/env python3
import time
from monitoring import FileMonitor, monitor_processes
from detection import detect_ransomware
from alert_system import send_alert, log_event
from encryption import encrypt_file
from tagging import tag_sensitive_files


class RansomwareDefender:
    def __init__(self):
        self.file_monitor = FileMonitor()
        self.running = False

    def start(self):
        """Start all monitoring services"""
        self.running = True
        self.file_monitor.start()
        log_event("System started: Monitoring active")

        try:
            while self.running:
                self._check_threats()
                time.sleep(5)  # Reduce CPU usage
        except KeyboardInterrupt:
            self.stop()

    def _check_threats(self):
        """Core threat detection logic"""
        if monitor_processes() or detect_ransomware():
            log_event("Ransomware behavior detected!")
            self._trigger_protection()

    def _trigger_protection(self):
        """Execute protective measures"""
        send_alert()
        for file_path in self.file_monitor.sensitive_files:
            if tag_sensitive_files(file_path):  # Double-check sensitivity
                encrypt_file(file_path)
                log_event(f"Protected: {file_path}")

    def stop(self):
        """Graceful shutdown"""
        self.running = False
        self.file_monitor.stop()
        log_event("System stopped")


if __name__ == "__main__":
    defender = RansomwareDefender()
    defender.start()