# Generated by Django 3.2.8 on 2023-03-14 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='site',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('prefix', models.CharField(max_length=64, unique=True, verbose_name='prefix')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('last_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('last_updated_by', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='state_master',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='State Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('last_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('last_updated_by', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='user_profile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(blank=True, max_length=6, null=True)),
                ('contact', models.CharField(max_length=10, unique=True)),
                ('alternate_contact', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='Upload_Images/userProfileImages/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('last_updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('last_updated_by', models.CharField(max_length=100)),
                ('allowed_sites', models.ManyToManyField(default=None, to='nhp_app.site')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nhp_app.state_master', verbose_name='state')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AddField(
            model_name='site',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nhp_app.state_master', verbose_name='state'),
        ),
    ]