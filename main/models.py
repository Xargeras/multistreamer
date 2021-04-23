from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db import models
from PIL import Image


class Avatar(models.Model):
    objects = None
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)  # Open image using self

        if img.height > 400 or img.width > 400:
            m = min(img.height, img.weight)
            new_img = img.crop(
                (img.width // 2 - 200,
                 img.height // 2 - 200,
                 img.width // 2 + 200,
                 img.height // 2 + 200))
            new_img = new_img.resize(400, 400)
            new_img.save(self.image.path)  # saving image at the same path


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
