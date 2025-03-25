# auth_utils.py
import ast
from werkzeug.security import generate_password_hash, check_password_hash
from config import USER_DB

def load_users():
    with open(USER_DB, 'r') as f:
        return ast.literal_eval(f.read())

def save_users(users):
    with open(USER_DB, 'w') as f:
        f.write(str(users))

def register_user(username, password):
    users = load_users()
    if username in users:
        return False  # User exists
    users[username] = generate_password_hash(password)
    save_users(users)
    return True

def authenticate(username, password):
    users = load_users()
    if username in users and check_password_hash(users[username], password):
        return True
    return False