from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY_PATH
import Pyfhel  # Homomorphic encryption library

def generate_key():
    """
    Generate and save an encryption key.
    """
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_PATH, 'wb') as key_file:
        key_file.write(key)

def load_key():
    """
    Load the encryption key.
    """
    with open(ENCRYPTION_KEY_PATH, 'rb') as key_file:
        return key_file.read()

def encrypt_file(file_path):
    """
    Encrypt a file using AES-256.
    """
    key = load_key()
    cipher_suite = Fernet(key)
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = cipher_suite.encrypt(data)
        with open(file_path, 'wb') as f:
            f.write(encrypted_data)
        log_event(f"Encrypted file: {file_path}")
    except Exception as e:
        log_event(f"Failed to encrypt file {file_path}: {e}")

def homomorphic_encrypt(data):
    """
    Encrypt data using homomorphic encryption.
    """
    HE = Pyfhel.Pyfhel()
    HE.contextGen(scheme='bfv', n=4096, t_bits=20)
    HE.keyGen()
    encrypted_data = HE.encryptInt(data)
    return encrypted_data, HE

def homomorphic_decrypt(encrypted_data, HE):
    """
    Decrypt data using homomorphic encryption.
    """
    return HE.decryptInt(encrypted_data)