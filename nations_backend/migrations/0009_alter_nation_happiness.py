# Generated by Django 5.0.1 on 2024-01-25 20:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nations_backend', '0008_alter_nation_taxes_to_collect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nation',
            name='happiness',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(10)]),
        ),
    ]