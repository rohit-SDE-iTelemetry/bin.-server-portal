# Generated by Django 3.2.8 on 2023-04-06 10:30

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nhp_app', '0015_alter_site_last_reading'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='last_readings',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='site',
            name='last_reading',
            field=models.TextField(blank=True, null=True),
        ),
    ]