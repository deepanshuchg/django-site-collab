from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import urllib.request, json


# Create your views here.
def index(request):
    return render(request, 'users/index.html')


def login(request):
    return render(request, 'users/login.html')


def logout(request):
    return render(request, 'users/logout.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Your account has been created, please Log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def youtube(request):
    if request.method == "POST":
        channel_name = request.POST.get('channel_name')
        channel_id = request.POST.get('channel_id')
        if channel_id == "":                                #Considering Channel name is entered

            search_url = 'https://www.googleapis.com/youtube/v3/channels'

            params = {
                'part': 'snippet,contentDetails,statistics',
                'forUsername': channel_name,
                'key': settings.YOUTUBE_DATA_API_KEY,
            }

            res_channel = requests.get(search_url, params=params)
            playlist_id = res_channel.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            playlist_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
            params_playlist = {
                'part': 'snippet,contentDetails',
                'playlistId': playlist_id,
                'key': settings.YOUTUBE_DATA_API_KEY

            }

            videos = []
            next_page_token = None
            # while 1:
            #    res = requests.get(search_url,playlistId = playlist_id,
            #                  part = 'snippet',
            #                  maxresult='10',
            #                       pageToken = next_page_token)
            #    videos += res['items']
            #    next_page_token = res['nextPageToken']
            #
            #    if next_page_token is None:
            #     break
            # print(videos)
            res_playlist = requests.get(playlist_url, params=params_playlist)
            print(res_playlist.text)
    
        else:       #Considering channel ID is entered

            search_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={settings.YOUTUBE_DATA_API_KEY}"
            data = urllib.request.urlopen(search_url).read()

            subscribers = json.loads(data)['items'][0]['statistics']['subscriberCount']
            total_videos = json.loads(data)['items'][0]['statistics']['videoCount']
            total_views = json.loads(data)['items'][0]['statistics']['viewCount']

            print(f"\nTotal number of subscribers: {subscribers}")
            print(f"Total number of videos uploaded: {total_videos}")
            print(f"Total views on the channel: {total_views}\n")

    return render(request, 'users/youtube.html')
