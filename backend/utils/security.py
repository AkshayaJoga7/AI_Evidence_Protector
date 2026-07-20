import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

def hash_password(password: str) -> str:
    """Generate password hash using Werkzeug security."""
    return generate_password_hash(password)

def verify_password(p_hash: str, password: str) -> bool:
    """Verify password against stored hash."""
    return check_password_hash(p_hash, password)

def generate_file_sha256(file_path: str) -> str:
    """Generate SHA-256 digital signature of a file for evidence integrity."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_api_token() -> str:
    """Generate secure random string token."""
    return secrets.token_hex(32)
