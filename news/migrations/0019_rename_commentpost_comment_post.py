# Generated by Django 4.2 on 2023-08-16 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0018_alter_comment_options_remove_comment_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='commentPost',
            new_name='post',
        ),
    ]
