# django-admin-large-initial-data
Allow to make redirects with large session data.

This application overrides limitation of Django ModelAdmin.get_changeform_initial_data which
 is encoded in URL and therefore limmited in size.

With `django-admin-large-initial-data`, You can make redirections to the
 ModelAdmin with large set of data marked as ManyToManyField.


# Basic Usage

In Admin use `LargeInitialMixin`:
```Python
   from large_initial import LargeInitialMixin
   @admin.register(models.Album)
   class AlbumAdmin(LargeInitialMixin, admin.ModelAdmin):
       pass
```

Then you can create redirection link:
```Python
   from large_initial import build_redirect_url

   address = build_redirect_url(
       request,
       'admin:main_album_add',
       params={'artists': musicians},
   )
```
all of the `musicians` objects are stored in `request.session`.
