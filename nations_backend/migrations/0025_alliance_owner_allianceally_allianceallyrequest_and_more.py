# Generated by Django 5.0.1 on 2024-09-21 21:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nations_backend', '0024_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='alliance',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alliance_owner', to='nations_backend.nation'),
        ),
        migrations.CreateModel(
            name='AllianceAlly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accepted_allies', to='nations_backend.alliance')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nations_backend.alliance')),
            ],
        ),
        migrations.CreateModel(
            name='AllianceAllyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.IntegerField()),
                ('alliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nations_backend.alliance')),
                ('requesting_alliance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to='nations_backend.alliance')),
            ],
        ),
        migrations.CreateModel(
            name='AllianceEnemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aggressor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nations_backend.alliance')),
                ('enemy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enemies', to='nations_backend.alliance')),
            ],
        ),
    ]
