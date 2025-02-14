from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY_PATH

def load_key():
    with open(ENCRYPTION_KEY_PATH, 'rb') as key_file:
        return key_file.read()

def decrypt_file(file_path):
    key = load_key()
    cipher_suite = Fernet(key)
    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        with open(file_path, 'wb') as f:
            f.write(decrypted_data)
        print(f"Decrypted file: {file_path}")
    except Exception as e:
        print(f"Failed to decrypt file {file_path}: {e}")