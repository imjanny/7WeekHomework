# Generated by Django 4.2 on 2023-04-27 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='user_id',
            new_name='user',
        ),
    ]
