from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db import models


class Avatar(models.Model):
    objects = None
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True)


class InputBroadcast(models.Model):
    RTSP = 1
    RTMP = 2
    choices = [
        (RTSP, 'RTSP'),
        (RTMP, 'RTMP'),
    ]
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=128, default="")
    type = models.IntegerField(choices=choices, default=RTSP)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OutputBroadcast(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128, validators=[URLValidator(schemes=['http', 'https', 'ftp', 'ftps', 'rtmp'])])
    key = models.CharField(max_length=128, default="")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    input_broadcast = models.ForeignKey(to=InputBroadcast, on_delete=models.CASCADE, blank=False, default=1)
