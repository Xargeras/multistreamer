from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db import models
from PIL import Image


class Avatar(models.Model):
    objects = None
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True)

    def save(self):
        super().save()  # saving image first

        img = Image.open(self.image.path)  # Open image using self

        if img.height > 400 or img.width > 400:
            new_img = (400, 400)
            ##img.thumbnail(new_img)
            new_img = img.crop(img.width // 2 - 200, img.height // 2 - 200, img.width // 2 + 200, img.height // 2 + 200)
            img.save(self.image.path)  # saving image at the same path


class InputBroadcast(models.Model):
    url = models.URLField(max_length=128, default="")
    key = models.CharField(max_length=128, default="")


class OutputBroadcast(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128, validators=[URLValidator(schemes=['http', 'https', 'ftp', 'ftps', 'rtmp'])])
    key = models.CharField(max_length=128, default="")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    broadcast = models.ForeignKey(to=InputBroadcast, on_delete=models.CASCADE)
