# Generated by Django 4.2.3 on 2025-03-16 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='google_books_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
