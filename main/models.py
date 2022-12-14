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
            middle = min(img.height, img.width)
            new_img = img.crop(
                ((img.width - middle) // 2,
                 (img.height - middle) // 2,
                 img.width - (img.width - middle) // 2,
                 img.height - (img.height - middle) // 2))
            new_img = new_img.resize((400, 400))
            new_img.save(self.image.path)  # saving image at the same path


class InputBroadcast(models.Model):
    RTSP = 1
    RTMP = 2
    choices = [
        (RTSP, 'RTSP'),
        (RTMP, 'RTMP'),
    ]
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=128, default='')
    type = models.IntegerField(choices=choices, default=RTSP)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OutputBroadcast(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128,
                           validators=[URLValidator(
                               schemes=['http', 'https', 'ftp', 'ftps', 'rtmp']
                           )])
    key = models.CharField(max_length=128, default='')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    bitrate = models.IntegerField(default=2300)
    is_active = models.BooleanField(default=False)
    input_broadcast = models.ForeignKey(to=InputBroadcast,
                                        on_delete=models.CASCADE,
                                        blank=False, default=1)


class YoutubeSettings(models.Model):
    p1440 = 0
    p1080 = 1
    p720 = 2
    p480 = 3
    p360 = 4
    public = 0
    private = 1
    choices = [
        (p1440, '1440p'),
        (p1080, '1080p'),
        (p720, '720p'),
        (p480, '480p'),
        (p360, '360p'),
    ]
    privacy_choices = [
        (public, 'public'),
        (private, 'private'),
    ]
    #youtube
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    resolution = models.IntegerField(choices=choices, default=0)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    privacy = models.IntegerField(choices=privacy_choices, default=0)
    user_credentials = models.JSONField(null=True)
    #broadcast
    name = models.CharField(max_length=128)
    bitrate = models.IntegerField(default=20000)
    is_active = models.BooleanField(default=False)
    url = models.CharField(max_length=128, default='rtmp://a.rtmp.youtube.com/live2')
    key = models.CharField(max_length=128, default='')
    input_broadcast = models.ForeignKey(to=InputBroadcast, on_delete=models.CASCADE, blank=False, default=1)
