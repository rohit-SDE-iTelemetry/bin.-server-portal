# Generated by Django 3.2.8 on 2023-04-06 10:29

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nhp_app', '0014_alter_site_last_reading'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='last_reading',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
