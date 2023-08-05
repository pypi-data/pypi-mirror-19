
from django.db import models


class Musician(models.Model):
    name = models.CharField(max_length=50)


class Album(models.Model):
    artists = models.ManyToManyField(Musician)
