from django.db import models
import django.utils.timezone
from book_manage.models import Book

# Create your models here.
class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, default='')
    start_time = models.DateTimeField(auto_now_add=True)
    linked_books = models.ManyToManyField(Book)