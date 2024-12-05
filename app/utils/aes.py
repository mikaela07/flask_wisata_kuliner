from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os

class AESCipher:
    def __init__(self):
        secret_key = os.getenv('AES_KEY', 'YourSecretKey123')
        self.key = self._prepare_key(secret_key)

    def _prepare_key(self, key_string):
        key_bytes = key_string.encode('utf-8')
        return pad(key_bytes, AES.block_size)[:32]

    def encrypt_password(self, raw_password):
        if not raw_password:
            return None
        
        try:
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            padded_data = pad(raw_password.encode('utf-8'), AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            encrypted_package = iv + encrypted_data
            return base64.b64encode(encrypted_package).decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")
            return None

    def decrypt_password(self, encrypted_text):
        if not encrypted_text:
            return None
            
        try:
            encrypted_package = base64.b64decode(encrypted_text.encode('utf-8'))
            iv = encrypted_package[:AES.block_size]
            encrypted_data = encrypted_package[AES.block_size:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_padded = cipher.decrypt(encrypted_data)
            decrypted_data = unpad(decrypted_padded, AES.block_size)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return None