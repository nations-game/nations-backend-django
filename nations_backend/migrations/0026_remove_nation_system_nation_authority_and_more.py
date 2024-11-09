# Generated by Django 5.0.1 on 2024-11-09 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nations_backend', '0025_alliance_owner_allianceally_allianceallyrequest_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nation',
            name='system',
        ),
        migrations.AddField(
            model_name='nation',
            name='authority',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nation',
            name='economic',
            field=models.IntegerField(default=0),
        ),
    ]
