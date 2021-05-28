from typing import Sized
from pytube import YouTube, streams
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image

root = Tk()
root.title("YouTube Downloader")
folder = " " 

logoYtb = Image.open("youtube.png")
resizeLogo = logoYtb.resize((200, 100))
img = ImageTk.PhotoImage(resizeLogo)
logo = Label(image=img)
logo.image = img
logo.pack()




urlLabel = Label(root,text="Enter URL Video")
urlLabel.pack()
url = StringVar()
urlEntry = Entry(root,textvariable=url, width=50)
urlEntry.pack()
checkUrl = Label(root,text="",fg="red")
checkUrl.pack()

dwnloadLabel = Label(root,text="Choose video/audio")
dwnloadLabel.pack()
kind = ["480p", "Only audio"]
dwnload=ttk.Combobox(root, values=kind)
dwnload.pack(pady=5)


checkLoc = Label(root,text="",fg="red")
checkLoc.pack()
def location():
    global folder
    folder=filedialog.askdirectory()
    if(len(folder) > 1):
        checkLoc.config(text=folder,fg="black")

    else:
        checkLoc.config(text="Location Folder not Found!",fg="red")

save = Button(root,text="Save in",width=20,command=location)
save.pack(pady=10)

def download():
    choice = dwnload.get()
    url = urlEntry.get()
    if(len(url)>1):
        checkUrl.config(text=" ")
        ytb = YouTube(url)
        if choice == kind[0]:
            select = ytb.streams.filter(progressive=True).first()
        elif choice == kind[1]:
            select = ytb.streams.filter(only_audio=True).first()
        else:
            checkUrl.config(text="Link was not found!",fg="red")
    checkUrl.config(text="Download Succesfull")
    select.download(folder)
downloadbtn = Button(root,text="Donwload",width=20,command=download)
downloadbtn.pack()
  



root.mainloop()