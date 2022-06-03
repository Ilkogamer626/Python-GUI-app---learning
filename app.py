import tkinter as tk
from tkinter import ttk

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
text = tk.StringVar(value='Song name')
inputField = ttk.Entry(root, textvariable=text)
inputField.pack()

# printing input on the screen


def buttonClicked():
    writtenText = text.get()
    message.config(text=writtenText)


button = ttk.Button(root, text='Read', command=buttonClicked)
button.pack()

root.mainloop()
