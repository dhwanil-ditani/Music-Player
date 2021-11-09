from django.utils import timezone
from django.db import models
from accounts.models import User


class Song(models.Model):
    Language_Choice = (
        ('Hindi', 'Hindi'),
        ('English', 'English'),
    )
    name = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    language = models.CharField(max_length=20, choices=Language_Choice, default='Hindi')
    year = models.IntegerField()
    artist = models.CharField(max_length=200)
    song_file = models.FileField(upload_to='music/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    added_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.name, self.song)


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
