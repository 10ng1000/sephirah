# Generated by Django 4.2.9 on 2024-01-29 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_manage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='name',
            new_name='title',
        ),
    ]
