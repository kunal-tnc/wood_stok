# Generated by Django 5.0.3 on 2024-04-03 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_rename_height_finishedlog_thickness"),
    ]

    operations = [
        migrations.AddField(
            model_name="finishedlog",
            name="reference_id",
            field=models.CharField(blank=True, null=True),
        ),
    ]
