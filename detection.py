# detection.py
import pickle
import numpy as np
from config import MODEL_PATHS


class ThreatDetector:
    def __init__(self):
        self.scaler = self._load_model(MODEL_PATHS['scaler'])
        self.model = self._load_model(MODEL_PATHS['model'])
        self.metadata = self._load_model(MODEL_PATHS['metadata'])
        self.feature_names = self.metadata['feature_names']

    def _load_model(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def prepare_features(self, system_metrics):
        """Prepare and scale features in correct order"""
        features = []
        for feature in self.feature_names:
            features.append(system_metrics[feature])
        return self.scaler.transform([features])

    def detect(self, system_metrics):
        """Run full detection pipeline"""
        try:
            features = self.prepare_features(system_metrics)
            prediction = self.model.predict(features)
            return prediction[0] == 1  # True if ransomware
        except Exception as e:
            print(f"Detection error: {e}")
            return False