# Generated by Django 4.2 on 2023-07-23 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_post_book_alter_post_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='book',
        ),
    ]