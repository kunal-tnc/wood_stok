# Generated by Django 5.0.3 on 2024-04-05 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0025_container_a_navg_container_number_pieces_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="container",
            old_name="number_pieces",
            new_name="total_pieces",
        ),
    ]
