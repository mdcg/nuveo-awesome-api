# Generated by Django 2.2.6 on 2019-11-02 03:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191101_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='steps',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), size=None),
        ),
    ]
