from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    mail_id = models.IntegerField(null=True, default=None)
    
class Job(models.Model):
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="jobs")

    def __str__(self):
        return self.title