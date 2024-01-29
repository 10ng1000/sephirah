from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='books')

    def __str__(self):
        return self.title
