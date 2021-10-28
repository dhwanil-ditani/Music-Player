from django.urls import path
from musicapp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:song_id>/', views.detail, name='detail'),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/<str:name>/', views.playlist_songs, name='playlist_songs'),
    path('favourite/', views.favourite, name='favourite'),
    path('all_songs/', views.all_songs, name='all_songs'),
    path('recent/', views.recent, name='recent'),
    path('hindi_songs/', views.hindi_songs, name='hindi_songs'),
    path('english_songs/', views.english_songs, name='english_songs'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('play_song/<int:song_id>/', views.play_song_index, name='play_song_index'),
    path('play_recent_song/<int:song_id>/', views.play_recent_song, name='play_recent_song'),
]