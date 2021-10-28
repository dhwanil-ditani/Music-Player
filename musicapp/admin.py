from django.contrib import admin
from .models import Song, Recent, Playlist


admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Recent)
