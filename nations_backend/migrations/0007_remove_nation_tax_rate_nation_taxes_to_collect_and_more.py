# Generated by Django 5.0.1 on 2024-01-25 18:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nations_backend', '0006_remove_nationfactory_produced_commodities_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nation',
            name='tax_rate',
        ),
        migrations.AddField(
            model_name='nation',
            name='taxes_to_collect',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='nationfactory',
            name='ticks_run',
            field=models.IntegerField(default=3, validators=[django.core.validators.MaxValueValidator(24)]),
        ),
    ]
