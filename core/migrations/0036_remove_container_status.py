# Generated by Django 5.0.3 on 2024-04-18 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0035_container_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="container",
            name="status",
        ),
    ]
