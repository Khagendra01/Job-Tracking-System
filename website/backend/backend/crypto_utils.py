from cryptography.fernet import Fernet
from django.conf import settings
import base64

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message):
    key = settings.ENCRYPTION_KEY
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return base64.urlsafe_b64encode(encrypted_message).decode()

def decrypt_message(encrypted_message):
    key = settings.ENCRYPTION_KEY
    f = Fernet(key)
    decrypted_message = f.decrypt(base64.urlsafe_b64decode(encrypted_message))
    return decrypted_message.decode()