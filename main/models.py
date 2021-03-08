from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    objects = None
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True)


class InputBroadcast(models.Model):
    url = models.URLField(max_length=128)
    key = models.CharField(max_length=128)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)


class OutputBroadcast(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField(max_length=128)
    key = models.CharField(max_length=128)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    input = models.ForeignKey(to=InputBroadcast, on_delete=models.CASCADE)
