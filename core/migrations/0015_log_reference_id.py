# Generated by Django 5.0.3 on 2024-04-03 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_finishedlog_reference_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="log",
            name="reference_id",
            field=models.CharField(blank=True, null=True),
        ),
    ]
