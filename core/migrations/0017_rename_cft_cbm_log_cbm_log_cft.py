# Generated by Django 5.0.3 on 2024-04-03 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_finishedlog_reference_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='cft_cbm',
            new_name='cbm',
        ),
        migrations.AddField(
            model_name='log',
            name='cft',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True),
        ),
    ]