# Generated by Django 4.2 on 2023-08-25 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_remove_comment_status_alter_comment_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(choices=[('R', 'Отклонена'), ('A', 'Принята')], default='A'),
        ),
    ]