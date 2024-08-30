# Generated by Django 5.0.1 on 2024-08-27 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nations_backend', '0020_nation_land'),
    ]

    operations = [
        migrations.CreateModel(
            name='NationUpgrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upgrade_type', models.CharField(max_length=100)),
                ('level', models.IntegerField(default=1)),
                ('nation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upgrades', to='nations_backend.nation')),
            ],
        ),
    ]