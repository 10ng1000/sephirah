from django.db import models

# Create your models here.
class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, primary_key=True)