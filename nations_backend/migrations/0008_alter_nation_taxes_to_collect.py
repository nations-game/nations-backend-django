# Generated by Django 5.0.1 on 2024-01-25 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nations_backend', '0007_remove_nation_tax_rate_nation_taxes_to_collect_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nation',
            name='taxes_to_collect',
            field=models.IntegerField(),
        ),
    ]
