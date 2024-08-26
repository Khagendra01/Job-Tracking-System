from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Job
from rest_framework.exceptions import ValidationError
from .tasks import fetch_job_updates

import imaplib

User = get_user_model()

def is_OK(user, password):
    try:
        imap_url = 'imap.gmail.com'
        with imaplib.IMAP4_SSL(imap_url) as my_mail:
            my_mail.login(user, password)
        return True
    except (imaplib.IMAP4.error, Exception) as e:
        print(f"Error validating credentials: {e}")
        return False
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "username", "password", "mail_id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')

        if is_OK(username, password):
            validated_data['mail_id'] = None
            user = User.objects.create_user(**validated_data)

            return user
        else:
            raise ValidationError("Username or password is not valid.")

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "title", "status", "company", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}