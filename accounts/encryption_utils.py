from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

KEY = get_random_bytes(32)  # 32 bytes for AES-256
IV = get_random_bytes(16)  # 16 bytes for AES block cipher

def encrypt(plain_text):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt(encrypted_text):
    encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return unpad(cipher.decrypt(encrypted_bytes), AES.block_size).decode('utf-8')