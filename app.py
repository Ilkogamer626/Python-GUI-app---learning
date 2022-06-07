import tkinter as tk
from tkinter import E, EW, W, StringVar, Text, ttk
from turtle import bgcolor
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
import shutil
import numpy as np
import os


root = tk.Tk()
root.title('Give me!')
windowWidth = 1200
windowHeight = 600
canvas = tk.Canvas(root, width=windowWidth, height=windowHeight)
canvas.grid(columnspan=6, rowspan=4)

# centering the window
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

xOffset = int(screenWidth/2 - windowWidth/2)
yOffset = int(screenHeight/2 - windowHeight/2)
root.geometry(f'{windowWidth}x{windowHeight}+{xOffset}+{yOffset-100}')


musicbrainzngs.set_useragent('GiveMe!', '0.1', contact=None)


def buttonClicked():
    writtenText = text.get()
    if(writtenText):
        toBeAddedIntoUrl = slugify(
            writtenText, separator='%20') + '%20' + slugify(artist.get(), separator='%20')
        httpUrl = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={toBeAddedIntoUrl}&key=AIzaSyCf6bBW5Ujtp1vOF0ycQO6cKtYSUBMa5ps'
        response = requests.get(
            httpUrl)
        responseObject = response.json()
        youtubeId = responseObject["items"][0]['id']['videoId']
        urlToDownload = f'https://youtu.be/{youtubeId}'
        arrayToPass = [urlToDownload]
        # downloadFromYoutube(arrayToPass)
        modifyMetadata()
        # moveSong()


def downloadFromYoutube(arrayOfURlsToDownload):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
                   'preferredcodec': 'mp3',
                   'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(arrayOfURlsToDownload)


def moveSong():
    listOfSongs = listFilenames()
    onlyThisSong = listOfSongs[0]
    shutil.move(
        onlyThisSong, 'C:/Users/nasta/Desktop/Projects/Python GUI app - learning/Done')

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


def findArtist():
    artistName = artist.get()
    artistResponse = musicbrainzngs.search_artists(artistName, 10)
    artistId = getTheRightArtist(artistResponse['artist-list'], artistName)
    artistToReturn: str = artistId
    return artistToReturn


def getTheRightArtist(artistList, theNameWeAreLookingFor):
    for n in range(10):
        if(artistList[n]['name'] == theNameWeAreLookingFor):
            return artistList[n]['id']


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
        musicMetadata['tracknumber'] = tracknumber
    musicMetadata.save()
    splitStr = hopefullyOnlyThisSong.split('\\')
    splitStr.reverse()
    splitStr[0] = f'{musicMetadata["title"][0]}.mp3'
    splitStr.reverse()
    destStr = '\\'.join(x for x in splitStr)
    os.rename(hopefullyOnlyThisSong, destStr)


button = tk.Button(root, text='Give me:',
                   command=buttonClicked, bg='#599e7e', fg='#ffffff', width=20)
button.grid(column=1, row=1)

text = tk.StringVar(value='')
inputField = ttk.Entry(root, textvariable=text, width=30)
inputField.grid(column=2, row=1, sticky=EW,)

fromLabel = ttk.Label(root, text='By')
fromLabel.grid(column=3, row=1)

artist = StringVar(value='')
artistInput = ttk.Entry(root, textvariable=artist, width=30)
artistInput.grid(column=4, row=1, sticky=EW,)


root.mainloop()


# https://www.youtube.com/results?search_query=big+iron
# GET https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=big%20iron&key=[YOUR_API_KEY] HTTP/1.1
# AIzaSyCf6bBW5Ujtp1vOF0ycQO6cKtYSUBMa5ps
# https://musicbrainz.org/ws/2/
# /<ENTITY_TYPE>?query=<QUERY>&limit=<LIMIT>&offset=<OFFSET>
#  https://musicbrainz.org/ws/2/recording?query=%22we%20will%20rock%20you%22%20AND%20arid:0383dadf-2a4e-4d10-a46a-e9e041da8eb3
