# Generated by Django 5.0.2 on 2024-02-22 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_rename_liked_like_delete_disliked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='object_id',
            new_name='content_id',
        ),
    ]