# Generated by Django 5.0.3 on 2024-03-19 18:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('message', models.TextField(verbose_name='message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('seen', models.BooleanField(default=False, verbose_name='seen')),
                ('date_seen', models.DateTimeField(blank=True, null=True, verbose_name='date seen')),
                ('resolved', models.BooleanField(default=False, verbose_name='resolved')),
                ('date_resolved', models.DateTimeField(blank=True, null=True, verbose_name='date resolved')),
                ('resolved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_by', to=settings.AUTH_USER_MODEL)),
                ('seen_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='seen_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'complaint',
                'verbose_name_plural': 'complaints',
            },
        ),
    ]
