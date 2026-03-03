import hashlib
import secrets
# Hasher class
class PasswordHasher:
    def hash_password(self, password):
        """Hash password with random salt using PBKDF2"""
        salt = secrets.token_bytes(32)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # 100,000 iterations for security
        )
        return password_hash, salt
    # Verifies
    def verify_password(self, password, stored_hash, salt):
        """Verify password against stored hash"""
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return password_hash == stored_hash
