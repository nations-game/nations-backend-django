# Generated by Django 5.0.1 on 2024-09-07 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nations_backend', '0022_nation_unused_land'),
    ]

    operations = [
        migrations.CreateModel(
            name='NationDivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('nation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisions', to='nations_backend.nation')),
            ],
        ),
        migrations.CreateModel(
            name='DivisionUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(max_length=100)),
                ('health', models.IntegerField()),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='nations_backend.nationdivision')),
            ],
        ),
    ]
