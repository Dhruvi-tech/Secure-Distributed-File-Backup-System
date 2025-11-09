import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib

class EncryptionManager:
    """AES-256 encryption manager for files"""

    def __init__(self):
        self.backend = default_backend()
        self.key_size = 32  # 256 bits

    def generate_key(self) -> bytes:
        """Generate a random AES-256 key"""
        return os.urandom(self.key_size)

    def generate_key_b64(self) -> str:
        """Generate a random AES-256 key and return as base64 string"""
        return base64.b64encode(self.generate_key()).decode('utf-8')

    def key_from_b64(self, key_b64: str) -> bytes:
        """Convert base64 key back to bytes"""
        return base64.b64decode(key_b64)

    def encrypt_file(self, file_data: bytes, key: bytes) -> bytes:
        """Encrypt file data using AES-256-CBC"""
        # Generate random IV
        iv = os.urandom(16)

        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # Pad the data
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        # Encrypt
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Return IV + encrypted data
        return iv + encrypted_data

    def decrypt_file(self, encrypted_data: bytes, key: bytes) -> bytes:
        """Decrypt file data using AES-256-CBC"""
        if len(encrypted_data) < 16:
            raise ValueError("Encrypted data too short")

        # Extract IV and encrypted content
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        # Decrypt
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpad
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        original_data = unpadder.update(padded_data) + unpadder.finalize()

        return original_data

    def encrypt_chunk(self, chunk_data: bytes, key: bytes) -> bytes:
        """Encrypt a single chunk"""
        return self.encrypt_file(chunk_data, key)

    def decrypt_chunk(self, encrypted_chunk: bytes, key: bytes) -> bytes:
        """Decrypt a single chunk"""
        return self.decrypt_file(encrypted_chunk, key)

    def calculate_checksum(self, data: bytes) -> str:
        """Calculate MD5 checksum of data"""
        return hashlib.md5(data).hexdigest()

    def verify_checksum(self, data: bytes, expected_checksum: str) -> bool:
        """Verify data against expected checksum"""
        return self.calculate_checksum(data) == expected_checksum

# Global encryption manager instance
encryption_manager = EncryptionManager()