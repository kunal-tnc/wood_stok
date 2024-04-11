# Generated by Django 5.0.3 on 2024-04-10 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0026_rename_number_pieces_container_total_pieces"),
    ]

    operations = [
        migrations.AlterField(
            model_name="log",
            name="cbm",
            field=models.DecimalField(
                blank=True, decimal_places=1, default=0, max_digits=20, null=True
            ),
        ),
        migrations.AlterField(
            model_name="log",
            name="cft",
            field=models.DecimalField(
                blank=True, decimal_places=1, default=0, max_digits=20, null=True
            ),
        ),
    ]