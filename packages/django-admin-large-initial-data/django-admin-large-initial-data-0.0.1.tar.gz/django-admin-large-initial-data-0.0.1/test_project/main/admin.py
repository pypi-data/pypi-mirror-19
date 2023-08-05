from django.contrib import admin
from . import models
from large_initial import LargeInitialMixin


@admin.register(models.Album)
class AlbumAdmin(LargeInitialMixin, admin.ModelAdmin):
    pass
