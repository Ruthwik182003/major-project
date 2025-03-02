from werkzeug.security import generate_password_hash, check_password_hash

# Mock user database
users = {
    "admin": generate_password_hash("admin_password")
}

def authenticate(username, password):
    """
    Verify the username and password.
    """
    if username in users and check_password_hash(users[username], password):
        return True
    return False