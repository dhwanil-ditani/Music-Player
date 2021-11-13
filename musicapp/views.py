from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from musicapp.models import Song, Playlist, Recent


def index(request):
    qs_artists = Song.objects.values_list('artist').all()
    s_list = [s.split(',') for artist in qs_artists for s in artist]
    all_artists = sorted(list(set([s.strip() for artist in s_list for s in artist])))
    qs_languages = Song.objects.values_list('language').all()
    all_languages = sorted(list(set([l.strip() for lang in qs_languages for l in lang])))

    # Display recent songs
    if not request.user.is_anonymous:
        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        recent_id = [each['song_id'] for each in recent][:5]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id, recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent = None
        recent_songs = None

    first_time = False

    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
        else:
            first_time = True
            last_played_song = False

    else:
        first_time = True
        last_played_song = False

    # Display all songs
    songs = Song.objects.all()

    # Display few songs on home page
    songs_all = list(Song.objects.all().values('id').order_by('?'))
    sliced_ids = [each['id'] for each in songs_all][:6]
    indexpage_songs = Song.objects.filter(id__in=sliced_ids)

    # Display Hindi Songs
    songs_hindi = list(Song.objects.filter(language='Hindi').values('id'))
    sliced_ids = [each['id'] for each in songs_hindi][:6]
    indexpage_hindi_songs = Song.objects.filter(id__in=sliced_ids)

    # Display English Songs
    songs_english = list(Song.objects.filter(language='English').values('id'))
    sliced_ids = [each['id'] for each in songs_english][:6]
    indexpage_english_songs = Song.objects.filter(id__in=sliced_ids)
    context = {
        'all_artists': all_artists,
        'all_languages': all_languages,
        'all_songs': indexpage_songs,
        'recent_songs': recent_songs,
        'hindi_songs': indexpage_hindi_songs,
        'english_songs': indexpage_english_songs,
        'last_played': last_played_song,
        'first_time': first_time,
        'query_search': False,

    }
    return render(request, 'musicapp/index.html', context=context)


def all_songs(request):
    context = {}
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
            context['last_played'] = last_played_song
    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        search_singer = request.GET.get('artists') or ''
        search_language = request.GET.get('languages') or ''
        songs = Song.objects.filter(Q(name__icontains=search_query)).filter(
            Q(language__icontains=search_language)).filter(Q(artist__icontains=search_singer)).distinct()
        context['query_search'] = True
    else:
        songs = Song.objects.all()
    context['songs'] = songs
    qs_artists = Song.objects.values_list('artist').all()
    s_list = [s.split(',') for artist in qs_artists for s in artist]
    all_artists = sorted(list(set([s.strip() for artist in s_list for s in artist])))
    qs_languages = Song.objects.values_list('language').all()
    all_languages = sorted(list(set([l.strip() for lang in qs_languages for l in lang])))
    context['all_artists'] = all_artists
    context['all_languages'] = all_languages
    return render(request, 'musicapp/allsongs.html', context=context)


def hindi_songs(request):
    context = {}
    # Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = False
    query = request.GET.get('q')
    if query:
        hindi_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context['heading'] = 'SEARCH RESULTS'
    else:
        hindi_songs = Song.objects.filter(language='Hindi')
        context['heading'] = 'HINDI SONGS'
    qs_artists = Song.objects.values_list('artist').all()
    s_list = [s.split(',') for artist in qs_artists for s in artist]
    all_artists = sorted(list(set([s.strip() for artist in s_list for s in artist])))
    context['hindi_songs'] = hindi_songs
    context['all_artists'] = all_artists
    context['all_languages'] = ['Hindi']
    context['last_played'] = last_played_song
    return render(request, 'musicapp/hindi_songs.html', context=context)


def english_songs(request):
    context = {}
    # Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = False
    query = request.GET.get('q')
    if query:
        english_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context['heading'] = 'SEARCH RESULTS'
    else:
        english_songs = Song.objects.filter(language='English')
        context['heading'] = 'ENGLISH SONGS'
    qs_artists = Song.objects.values_list('artist').all()
    s_list = [s.split(',') for artist in qs_artists for s in artist]
    all_artists = sorted(list(set([s.strip() for artist in s_list for s in artist])))
    context['english_songs'] = english_songs
    context['all_artists'] = all_artists
    context['all_languages'] = ['English']
    context['last_played'] = last_played_song
    return render(request, 'musicapp/english_songs.html', context=context)


@login_required(login_url='login')
def play_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('all_songs')


@login_required(login_url='login')
def play_song_index(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('home')


@login_required(login_url='login')
def play_recent_song(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('recent')


def recent(request):
    # Last played song
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=2)
    # Display recent songs
    recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
    if recent and not request.user.is_anonymous:
        recent_id = [each['song_id'] for each in recent]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id, recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent_songs = None
    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = recent_songs_unsorted.filter(Q(name__icontains=search_query)).distinct()
        context = {'recent_songs': filtered_songs, 'last_played': last_played_song, 'query_search': True}
        return render(request, 'recent.html', context)
    context = {'recent_songs': recent_songs, 'last_played': last_played_song, 'query_search': False}
    return render(request, 'recent.html', context=context)


@login_required(login_url='login')
def playlist(request):
    playlists = Playlist.objects.filter(user=request.user).values('name').distinct()
    context = {'playlists': playlists}
    return render(request, 'musicapp/playlist.html', context=context)


@login_required(login_url='login')
def playlist_songs(request, name):
    songs = Song.objects.filter(playlist__name=name, playlist__user=request.user).distinct()
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(name=name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")
    context = {'name': name, 'songs': songs}
    return render(request, 'musicapp/playlist_songs.html', context=context)


def detail(request, song_id):
    songs = Song.objects.filter(id=song_id).first()
    playlists = Playlist.objects.filter(user=request.user).values('name').distinct
    is_fav = len(Playlist.objects.filter(user=request.user, song__id=song_id, name='favorite')) == 1
    context = {
        'songs': songs,
        'playlists': playlists,
        'is_favourite': is_fav,
    }

    last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
        context['last_played'] = last_played_song

    if request.method == "POST":
        if 'playlist' in request.POST:
            playlist_name = request.POST["playlist"]
            q = Playlist(user=request.user, song=songs, name=playlist_name)
            q.save()
            messages.success(request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            query = Playlist(user=request.user, song=songs, name='favorite')
            # print(f'query: {query}')
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('detail', song_id=song_id)
        elif 'rm-fav' in request.POST:
            query = Playlist.objects.filter(user=request.user, song__id=song_id, name='favorite')
            # print(f'user: {request.user}')
            # print(f'song: {songs.id} - {songs}')
            # print(f'query: {query}')
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('detail', song_id=song_id)

    return render(request, 'musicapp/details.html', context=context)


@login_required(login_url='login')
def favourite(request):
    playlist_name = 'favorite'
    songs = Song.objects.filter(playlist__user=request.user, playlist__name=playlist_name).distinct()
    print(f'songs: {songs}')
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        favourite_song = Playlist.objects.filter(user=request.user, song__id=song_id, playlist__name='favorite')
        favourite_song.delete()
        messages.success(request, "Removed from favourite!")
    context = {'songs': songs, 'playlist_name': playlist_name}
    return render(request, 'musicapp/favourite.html', context=context)
