# Generated by Django 4.1.1 on 2022-09-18 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0002_rename_file_song_music'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='release_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]