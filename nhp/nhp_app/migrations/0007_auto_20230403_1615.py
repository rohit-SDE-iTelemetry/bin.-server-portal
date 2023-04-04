# Generated by Django 3.2.8 on 2023-04-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nhp_app', '0006_rename_state_site_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='location',
        ),
        migrations.AddField(
            model_name='site',
            name='device_location',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]