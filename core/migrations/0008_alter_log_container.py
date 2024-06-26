# Generated by Django 5.0.3 on 2024-03-14 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_log_cft_cbm_alter_log_girth_alter_log_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="log",
            name="container",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="logs",
                to="core.container",
            ),
        ),
    ]
