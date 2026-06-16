import hashlib

def hash_password(password):
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, provided_password):
    """Verify a password against its hash."""
    return stored_hash == hash_password(provided_password)
