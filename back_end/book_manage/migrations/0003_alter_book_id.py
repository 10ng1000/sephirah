# Generated by Django 4.2.9 on 2024-01-29 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_manage', '0002_rename_name_book_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]