# models.py
from django.db import models
from django.contrib.auth.models import User
from .encryption_utils import encrypt, decrypt

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    encrypted_username = models.CharField(max_length=256)

    def set_username(self, username):
        self.encrypted_username = encrypt(username)

    def get_username(self):
        return decrypt(self.encrypted_username)

    def save(self, *args, **kwargs):
        # Encrypt the username before saving
        if self.user.username:
            self.set_username(self.user.username)
        super().save(*args, **kwargs)
