from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.conf import settings
from django.db.models import UniqueConstraint


class User(AbstractUser):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Flowers(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    image = models.ImageField(upload_to='images/')
    description = models.TextField(blank=True)  # images/Flowers


class SightingModel(BaseModel):
    sighting_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sighting_username') # readonly
    flower_id = models.IntegerField(Flowers, blank=False)
    quote = models.CharField(Flowers, max_length=255, blank=False, default='')
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/')  #images_sightings
    created_by = models.CharField(max_length=200)


class SightingLikes(models.Model):
    like = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='likesusername')
    sight = models.ForeignKey(SightingModel, on_delete=models.CASCADE, related_name='likes_andsighting')
    created_by = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        unique_together = [
            ("sight", "created_by"),
]

