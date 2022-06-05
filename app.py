import tkinter as tk
from tkinter import StringVar, Text, ttk
import requests
import json
from types import SimpleNamespace
import youtube_dl
from slugify import slugify
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
import musicbrainzngs
import glob

import numpy as np


root = tk.Tk()
root.title('Give me!')
windowWidth = 1200
windowHeight = 600

# centering the window
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

xOffset = int(screenWidth/2 - windowWidth/2)
yOffset = int(screenHeight/2 - windowHeight/2)
root.geometry(f'{windowWidth}x{windowHeight}+{xOffset}+{yOffset-100}')

# displaying a message
message = ttk.Label(root, text="Hello world")
message.pack()
musicbrainzngs.set_useragent('GiveMe!', '0.1', contact=None)

# getting input
text = tk.StringVar(value='')
inputField = ttk.Entry(root, textvariable=text)
inputField.pack()


def buttonClicked():
    writtenText = text.get()
    message.config(text=writtenText)
    if(writtenText):
        toBeAddedIntoUrl = slugify(
            writtenText, separator='%20') + '%20' + slugify(artist.get(), separator='%20')
        httpUrl = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={toBeAddedIntoUrl}&key=AIzaSyCf6bBW5Ujtp1vOF0ycQO6cKtYSUBMa5ps'
        response = requests.get(
            httpUrl)
        responseObject = response.json()
        youtubeId = responseObject["items"][0]['id']['videoId']

        # downloading the video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        urlToDownload = f'https://youtu.be/{youtubeId}'
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([urlToDownload])
        modifyMetadata()


button = ttk.Button(root, text='Give me:', command=buttonClicked)
button.pack()

# function for listing all the filenames in the directory


def listFilenames():
    listOfFilenames = glob.glob(
        'C:/Users/nasta/Desktop/Projects/Python GUI app - learning/*.mp3')
    return listOfFilenames
# function for finding the metadata


def findMetadata():
    modifiedText = slugify(text.get(), separator='%20')
    musicName = f'%22{modifiedText}%22'
    artistId = findArtist()
    foundSomething = requests.get(
        f'https://musicbrainz.org/ws/2/recording?query={musicName}%20AND%20arid:{artistId}&fmt=json&limit=1')
    workWithThis = foundSomething.json()
    return workWithThis['recordings'][0]


artist = StringVar(value='')
artistInput = ttk.Entry(root, textvariable=artist)
artistInput.pack()


def findArtist():
    artistName = slugify(artist.get(), separator='%20')
    artistResponse = musicbrainzngs.search_artists(artistName, 1, strict=True)
    artistToReturn: str = artistResponse['artist-list'][0]['id']
    return artistToReturn


def modifyMetadata():
    listA = listFilenames()
    hopefullyOnlyThisSong = listA[0]
    soonToBeMetadata = findMetadata()
    musicMetadata = MP3(hopefullyOnlyThisSong, ID3=EasyID3)
    musicMetadata['title'] = soonToBeMetadata['title']
    musicMetadata['artist'] = soonToBeMetadata['artist-credit'][0]['name']
    if(soonToBeMetadata['releases'][0]['release-group']['title'] != None):
        musicMetadata['album'] = soonToBeMetadata['releases'][0]['release-group']['title']
        musicMetadata['albumartist'] = soonToBeMetadata['releases'][0]['release-group']['title']
        tracknumber = str(soonToBeMetadata['releases'][0]['media'][0]['track'][0]['number']) + \
            '/' + str(soonToBeMetadata['releases'][0]['track-count'])
        print(tracknumber)
        musicMetadata['tracknumber'] = tracknumber
    musicMetadata.save()


root.mainloop()


# https://www.youtube.com/results?search_query=big+iron
# GET https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=big%20iron&key=[YOUR_API_KEY] HTTP/1.1
# AIzaSyCf6bBW5Ujtp1vOF0ycQO6cKtYSUBMa5ps
# https://musicbrainz.org/ws/2/
# /<ENTITY_TYPE>?query=<QUERY>&limit=<LIMIT>&offset=<OFFSET>
#  https://musicbrainz.org/ws/2/recording?query=%22we%20will%20rock%20you%22%20AND%20arid:0383dadf-2a4e-4d10-a46a-e9e041da8eb3
