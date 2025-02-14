import psutil
import pickle
from config import MODEL_PATH

def extract_features():
    cpu_usage = psutil.cpu_percent()
    disk_io = psutil.disk_io_counters()
    return [cpu_usage, disk_io.read_bytes, disk_io.write_bytes]

def detect_ransomware():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    features = extract_features()
    prediction = model.predict([features])
    return prediction[0] == 1  # 1 indicates ransomware