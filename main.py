# main.py
import time
from monitoring import FileMonitor, monitor_processes, get_system_metrics
from detection import ThreatDetector
from alert_system import send_alert, log_event
from encryption import encrypt_file


class RansomwareDefender:
    def __init__(self):
        self.file_monitor = FileMonitor()
        self.detector = ThreatDetector()
        self.running = False

    def start(self):
        """Start monitoring services"""
        self.running = True
        self.file_monitor.start()
        log_event("System started")

        try:
            while self.running:
                self._check_threats()
                time.sleep(5)
        except KeyboardInterrupt:
            self.stop()

    def _check_threats(self):
        """Check for ransomware using both models and heuristics"""
        system_metrics = get_system_metrics()
        if (self.detector.detect(system_metrics) or
                monitor_processes()):
            self._trigger_protection(system_metrics)

    def _trigger_protection(self, metrics):
        """Execute protection measures"""
        send_alert()
        log_event(f"Ransomware detected! Metrics: {metrics}")

        for file_path in self.file_monitor.sensitive_files:
            try:
                encrypt_file(file_path)
                metrics['encryption_calls'] += 1
                log_event(f"Encrypted: {file_path}")
            except Exception as e:
                log_event(f"Encryption failed for {file_path}: {str(e)}")

    def stop(self):
        """Graceful shutdown"""
        self.running = False
        self.file_monitor.stop()
        log_event("System stopped")


if __name__ == "__main__":
    defender = RansomwareDefender()
    defender.start()