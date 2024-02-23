# Generated by Django 5.0.2 on 2024-02-22 07:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_comment_dislikes_remove_post_dislikes_and_more'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Liked',
            new_name='Like',
        ),
        migrations.DeleteModel(
            name='Disliked',
        ),
    ]
