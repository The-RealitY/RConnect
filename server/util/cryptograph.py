import base64
import hashlib
import os
import secrets
from base64 import urlsafe_b64encode, urlsafe_b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class CryptoSecure:
    def __init__(self, secret_key: str):
        self._secret_key = self._generate_key(secret_key)

    @staticmethod
    def _generate_key(key_str):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(key_str.encode('UTF-8'))
        return urlsafe_b64encode(digest.finalize())

    @staticmethod
    def _generate_iv():
        return urlsafe_b64encode(os.urandom(16))

    def encrypt(self, msg: str):
        try:
            key = urlsafe_b64decode(self._secret_key)
            iv = urlsafe_b64decode(self._generate_iv())
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(msg.encode('UTF-8')) + encryptor.finalize()
            return urlsafe_b64encode(iv + ciphertext).decode('UTF-8')
        except Exception:
            return None

    def decrypt(self, enc_msg: str):
        try:
            key = urlsafe_b64decode(self._secret_key)
            data = urlsafe_b64decode(enc_msg)
            iv = data[:16]  # IV size is 16 bytes for AES
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decrypted = cipher.decryptor()
            dec_msg = decrypted.update(data[16:]) + decrypted.finalize()
            return dec_msg.decode('UTF-8')
        except Exception:
            return None

    @staticmethod
    def generate_hash(password):
        try:
            unq_salt = secrets.token_hex(16)
            hashed = hashlib.sha256(str(password + unq_salt).encode()).hexdigest()
            return f"{unq_salt}${hashed}"
        except Exception:
            return None

    @staticmethod
    def verify_hash(password, hash_str):
        try:
            salt, stored_hashed = hash_str.split('$', 1)
            input_hashed = hashlib.sha256((password + salt).encode()).hexdigest()
            return input_hashed == stored_hashed
        except Exception:
            return None

    @staticmethod
    def url_encode(string) -> str | None:
        try:
            return base64.b64encode(str(string).encode()).decode()
        except Exception:
            return None

    @staticmethod
    def url_decode(string) -> str | None:
        try:
            return base64.b64decode(string).decode()
        except Exception:
            return None
