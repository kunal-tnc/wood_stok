# Generated by Django 5.0.3 on 2024-04-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_container_a_navg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='a_navg',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='container',
            name='number_pieces',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='container',
            name='total_cbm',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]
