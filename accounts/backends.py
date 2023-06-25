# backends.py
import bcrypt
from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
from .encryption_utils import encrypt, decrypt

class CustomUserAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            custom_user = CustomUser.objects.get(encrypted_username=encrypt(username))
            user = custom_user.user
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):  # Check the password using bcrypt
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(user__pk=user_id).user
        except CustomUser.DoesNotExist:
            return None