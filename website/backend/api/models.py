from django.db import models
from django.contrib.auth.models import AbstractUser
from .crypto_utils import encrypt_value, decrypt_value

class CustomUser(AbstractUser):
    mail_id = models.IntegerField(null=True, default=None)
    web_pa = models.CharField(max_length=255, blank=True, null=True)
    def set_web_pa(self, password):
        if password:
            self.web_pa = encrypt_value(password)
        else:
            self.web_pa = None

    def get_web_pa(self):
        if self.web_pa:
            return decrypt_value(self.web_pa)
        return None
    
class Job(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="jobs")

    def __str__(self):
        return self.title