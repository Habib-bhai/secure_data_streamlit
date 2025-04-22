from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import hashlib

def hash_passkey(passkey: str) -> str:
    """Hash passkey for storage (not used for encryption)"""
    return hashlib.sha256(passkey.encode()).hexdigest()

def generate_salt() -> bytes:
    """Generate a random salt for PBKDF2"""
    return os.urandom(16)

def derive_key(passkey: str, salt: bytes) -> bytes:
    """Derive encryption key from passkey using PBKDF2"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passkey.encode()))

def encrypt_data(text: str, passkey: str, salt: bytes) -> str:
    """Encrypt data using passkey-derived key"""
    key = derive_key(passkey, salt)
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text: str, passkey: str, salt: bytes) -> str:
    """Decrypt data using passkey-derived key"""
    key = derive_key(passkey, salt)
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_text.encode()).decode()