# Generated by Django 5.1.6 on 2025-02-20 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
