from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY_PATH
from phe import paillier  # Homomorphic encryption library

def load_key():
    with open(ENCRYPTION_KEY_PATH, 'rb') as key_file:
        return key_file.read()

def encrypt_file(file_path):
    key = load_key()
    cipher_suite = Fernet(key)
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = cipher_suite.encrypt(data)
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
        print(f"Encrypted file: {file_path}")
    except Exception as e:
        print(f"Failed to encrypt file {file_path}: {e}")

def homomorphic_encrypt(data):
    public_key, private_key = paillier.generate_paillier_keypair()
    encrypted_data = public_key.encrypt(data)
    return encrypted_data, private_key