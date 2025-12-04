"""
Service for encrypting/decrypting OAuth tokens
"""
from cryptography.fernet import Fernet
from app.core.config import settings
import base64
import hashlib


def get_encryption_key() -> bytes:
    """Generate encryption key from secret key"""
    # Use secret key to derive encryption key
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_token(token: str) -> str:
    """Encrypt an OAuth token"""
    f = Fernet(get_encryption_key())
    return f.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt an OAuth token"""
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_token.encode()).decode()


