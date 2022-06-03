import tkinter as tk
from tkinter import ttk
import requests
import json
from types import SimpleNamespace
import youtube_dl
from slugify import slugify


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

# getting input
text = tk.StringVar(value='')
inputField = ttk.Entry(root, textvariable=text)
inputField.pack()

# printing input on the screen


def buttonClicked():
    writtenText = text.get()
    message.config(text=writtenText)
    if(writtenText):
        toBeAddedIntoUrl = slugify(writtenText, separator='%20')
        print(toBeAddedIntoUrl)
        httpUrl = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={toBeAddedIntoUrl}&key=AIzaSyCf6bBW5Ujtp1vOF0ycQO6cKtYSUBMa5ps'
        print(httpUrl)
        response = requests.get(
            httpUrl)
        responseObject = response.json()
        # I somehow need to transform dictionary or whatever to json I guess
        items = responseObject["items"]
        firstItem = items[0]
        firstItemId = firstItem['id']
        youtubeId = firstItemId['videoId']

        videoId = ttk.Label(root, text=youtubeId)
        videoId.pack()

        # downloading the video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        print(youtubeId)
        urlToDownload = f'https://youtu.be/{youtubeId}'
        print(urlToDownload)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([urlToDownload])


button = ttk.Button(root, text='Read', command=buttonClicked)
button.pack()


root.mainloop()


# https://www.youtube.com/results?search_query=big+iron
# GET https://youtube.googleapis.com/youtube/v3/search?part=snippet&q=big%20iron&key=[YOUR_API_KEY] HTTP/1.1
# AIzaSyCf6bBW5Ujtp1vOF0ycQO6cKtYSUBMa5ps
