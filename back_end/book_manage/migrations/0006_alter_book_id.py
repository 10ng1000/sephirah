# Generated by Django 4.2.9 on 2024-02-03 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_manage', '0005_book_chat_sessions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
