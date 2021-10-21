from django.utils import timezone
from django.db import models
from accounts.models import CustomUser

class Song(models.Model):

    Language_Choice = (
              ('Hindi', 'Hindi'),
              ('English', 'English'),
          )
    name = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    language = models.CharField(max_length=20,choices=Language_Choice,default='Hindi')
    year = models.IntegerField()
    artist = models.CharField(max_length=200)
    song_file = models.FileField(upload_to='music/')
    thunmbnail = models.ImageField(upload_to='thumbnails/')
    added_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Playlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Recent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)