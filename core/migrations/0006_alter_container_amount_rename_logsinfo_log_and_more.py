# Generated by Django 5.0.3 on 2024-03-14 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_logsinfo_container'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.RenameModel(
            old_name='LogsInfo',
            new_name='Log',
        ),
        migrations.CreateModel(
            name='FinishedLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Length (cm)')),
                ('width', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Width (cm)')),
                ('height', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Height (cm)')),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.log')),
            ],
        ),
    ]