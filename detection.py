import pickle

import psutil

from config import MODEL_PATH

def load_model():
    """
    Load the pre-trained ransomware detection model.
    """
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    return model

def detect_ransomware():
    """
    Detect ransomware using the pre-trained model.
    """
    model = load_model()
    features = extract_features()  # Extract features for detection
    prediction = model.predict([features])
    return prediction[0] == 1  # 1 indicates ransomware

def extract_features():
    """
    Extract system features for ransomware detection.
    """
    cpu_usage = psutil.cpu_percent()
    disk_io = psutil.disk_io_counters()
    return [cpu_usage, disk_io.read_bytes, disk_io.write_bytes]