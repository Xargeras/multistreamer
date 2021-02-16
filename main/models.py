from django.contrib.auth.models import User
from django.db import models


class Broadcast(models.Model):
    objects = None
    name = models.CharField(max_length=128)
    url = models.URLField(max_length=128)
    key = models.CharField(max_length=128)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
