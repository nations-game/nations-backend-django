# Generated by Django 5.0.1 on 2024-01-24 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nations_backend', '0003_alter_factorytype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nationfactory',
            name='factory_type',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='nationfactory',
            name='produced_commodities',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='FactoryType',
        ),
    ]