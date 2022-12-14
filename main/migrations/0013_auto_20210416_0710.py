# Generated by Django 3.1.6 on 2021-04-16 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20210416_0703'),
    ]

    operations = [
        migrations.AddField(
            model_name='outputbroadcast',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='inputbroadcast',
            name='type',
            field=models.IntegerField(choices=[(1, 'RTSP'), (2, 'RTMP')], default=1),
        ),
    ]
