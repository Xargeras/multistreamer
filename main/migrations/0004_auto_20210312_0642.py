# Generated by Django 3.1.6 on 2021-03-12 03:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210312_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outputbroadcast',
            name='url',
            field=models.URLField(max_length=128, validators=[django.core.validators.URLValidator(schemes=['http', 'https', 'ftp', 'ftps', 'rtmp'])]),
        ),
    ]
