# Generated by Django 2.2.6 on 2019-11-01 14:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='status',
            field=models.CharField(choices=[('inserted', 'inserted'), ('consumed', 'consumed')], default='inserted', max_length=8),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='steps',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), size=8),
        ),
    ]