# Generated by Django 3.1.6 on 2021-05-06 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_inputbroadcast_bitrate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inputbroadcast',
            name='bitrate',
        ),
        migrations.AddField(
            model_name='outputbroadcast',
            name='bitrate',
            field=models.IntegerField(default=2300),
        ),
    ]
