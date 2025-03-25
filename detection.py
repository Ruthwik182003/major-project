# detection.py
import os
import pickle
import numpy as np
import sklearn
from config import MODEL_PATHS
import xgboost


class ThreatDetector:
    def __init__(self):
        try:
            self.scaler = self._load_model(MODEL_PATHS['scaler'])
            self.model = self._load_model(MODEL_PATHS['model'])
            self.metadata = self._load_model(MODEL_PATHS['metadata'])
            self.feature_names = self.metadata.get('feature_names', [])
            print("✅ Models loaded successfully")
        except Exception as e:
            print(f"❌ Model loading failed: {str(e)}")
            raise

    def _load_model(self, path):
        if not os.path.exists(path):
            available = [f for f in os.listdir(os.path.dirname(path)) if f.endswith('.pkl')]
            raise FileNotFoundError(
                f"Model file not found at {path}\n"
                f"Available models: {available}"
            )
        with open(path, 'rb') as f:
            return pickle.load(f)

    # ... rest of your detection code ...
    def prepare_features(self, system_metrics):
        """Prepare and scale features with robust error handling"""
        try:
            # 1. Collect features in correct order
            features = []
            for feature in self.feature_names:
                features.append(system_metrics.get(feature, 0))  # Default to 0 if missing

            features_array = np.array(features).reshape(1, -1)

            # 2. Handle different scaler scenarios
            if isinstance(self.scaler, np.ndarray):
                # If scaler is accidentally an array, skip scaling
                print("Warning: Scaler is numpy array, using raw features")
                return features_array
            elif hasattr(self.scaler, 'transform'):
                # Normal case - proper scaler
                return self.scaler.transform(features_array)
            else:
                # Fallback
                print("Warning: Unexpected scaler type, using raw features")
                return features_array

        except Exception as e:
            print(f"Feature preparation error: {e}")
            return np.zeros((1, len(self.feature_names)))

    def detect(self, system_metrics):
        """Run full detection pipeline"""
        try:
            features = self.prepare_features(system_metrics)
            prediction = self.model.predict(features)
            return prediction[0] == 1  # True if ransomware
        except Exception as e:
            print(f"Detection error: {e}")
            return False