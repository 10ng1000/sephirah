from django.db import models

# Create your models here.
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    task_id = models.CharField(max_length=100, null=True)
    doccano_task_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name