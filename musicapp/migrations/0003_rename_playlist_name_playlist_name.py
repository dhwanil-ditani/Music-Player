# Generated by Django 3.2.8 on 2021-10-23 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0002_delete_favourite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='playlist_name',
            new_name='name',
        ),
    ]
