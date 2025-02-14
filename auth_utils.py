from flask import request, abort
import base64
from werkzeug.security import check_password_hash

# Mock user database (replace with your actual user storage)
users = {
    "admin": "hashed_password_here"  # Replace with a hashed password
}

def check_auth(username, password):
    """
    Verify the username and password.
    """
    if username in users and check_password_hash(users[username], password):
        return True
    return False

def authenticate():
    """
    Perform HTTP Basic Authentication.
    """
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Basic '):
        abort(401, "Unauthorized: Missing or invalid Authorization header")

    # Decode credentials
    encoded_credentials = auth.split(' ')[1]
    try:
        credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = credentials.split(':')
    except (ValueError, UnicodeDecodeError):
        abort(401, "Unauthorized: Invalid credentials format")

    # Verify credentials
    if not check_auth(username, password):
        abort(401, "Unauthorized: Invalid username or password")

    return username  # Return the username if authentication succeeds