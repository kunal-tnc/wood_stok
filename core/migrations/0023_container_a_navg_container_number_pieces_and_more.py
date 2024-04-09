# Generated by Django 5.0.3 on 2024-04-05 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_remove_container_a_navg_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="container",
            name="a_navg",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name="container",
            name="number_pieces",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="container",
            name="total_cbm",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=20, null=True
            ),
        ),
    ]
