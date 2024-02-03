from django.db import models
from chat.models import ChatSession
import uuid

# Create your models here.
class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='books')
    upload_time = models.DateTimeField(auto_now_add=True)
    #外键，关联chat_session表，多对多关系
    chat_sessions = models.ManyToManyField(ChatSession)

    def __str__(self):
        return self.title
