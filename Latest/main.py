import tkinter as tk
from tkinter import filedialog, Text
import pygame
import random

pygame.mixer.init()

canvHeight = 1000
canvWidth = 1000

onTrack = 0

tracks = []

root = tk.Tk()
pygame.init()

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

doLoopQueue = False
doLoopSong = False
started = False
paused = True
removeEntryText = None
doShuffle = False

originalPos = 0


def removeSong():
    global removeField
    global tracks
    print("removing song")
    try:
        i = int(removeField.get()) - 1
        tracks.remove(tracks[i])
        initList()
    except:
        print("invalid index " + str(i))
    removeField.delete(0, 'end')



def playAudio(firstTime=True):
    global fileBox
    global originalPos
    global tracks
    global onTrack
    global started
    global paused

    started = True
    if firstTime == True:
        updatePos()
        onTrack = 0
    fileBox.activate(index=onTrack)
    pygame.mixer.music.stop()
    print("play")
    button2 = tk.Button(buttonFrame, text="Pause", command=pauseAudio)
    button2.place(bordermode=tk.OUTSIDE, relheight=0.1, relwidth=0.35, relx=0.3, rely=0.5)
    originalPos = 0
    try:
        pygame.mixer.music.load(tracks[onTrack])
        pygame.mixer.music.play()
    except:
        if doLoopQueue:
            onTrack = 0
            pygame.mixer.music.load(tracks[onTrack])
            pygame.mixer.music.play()

    paused = False

def moveQueue():
    global onTrack
    global paused
    global doShuffle
    global tracks


    if pygame.mixer.music.get_busy() == False and started and not paused:
        if doLoopSong and not paused:
            playAudio(firstTime=False)
        elif doShuffle:
            onTrack = random.randint(0, len(tracks) - 1)
            print(onTrack)
            playAudio(firstTime=False)
        elif not doLoopSong:
            onTrack += 1
            playAudio(firstTime=False)

    root.after(100, moveQueue)


def loopQueueCommand():
    global doLoopQueue
    doLoopQueue = not doLoopQueue

def pauseAudio():
    print("pause")
    global paused
    global button2

    if paused == True:

        pygame.mixer.music.unpause()
        paused = False

        button2['text'] = "Pause"
    elif paused == False:
        pygame.mixer.music.pause()
        paused = True

        button2['text'] = "Unpause"

def setSong(event):
    global fileBox
    global onTrack
    global tracks

    onTrack = fileBox.curselection()[0]

    playAudio(firstTime=False)

    root.after(100, deselect)

def deselect():
    global fileBox

    fileBox.select_clear(first=0, last='end')


def addAudio():
    global tracks
    filenames = filedialog.askopenfilenames(parent=root, initialdir="/", title="Select File",
                                            filetypes=(('Music Files', '*.mp3 *.wav *.ogg *.xm *.mod'),))
    if filenames != '':
        tracks.extend(root.tk.splitlist(filenames))
    print(filenames)
    print(tracks)
    initList()

def updatePos():
    global originalPos
    global paused
    if not paused:
        originalPos += 1
        print("updated pos")
    root.after(1000, updatePos)

def fastForwardCommand():
    global originalPos
    pygame.mixer.music.set_pos(originalPos + 5)
    originalPos += 5

def fastBackwardCommand():
    global originalPos
    pygame.mixer.music.set_pos(originalPos + 5)
    originalPos -= 5

def initList():
    global tracks
    global fileBox
    i = 0
    fileBox.delete(0, 'end')
    for track in root.tk.splitlist(tracks):
        fileBox.insert(i, track)
        i += 1
    print(tracks)

def doShuffleCommand():
    global doShuffle

    doShuffle = not doShuffle

def setVol(i):
    pygame.mixer.music.set_volume(int(i)/100)

def loopSongCommand():
    global doLoopSong
    doLoopSong = not doLoopSong

def songForward():
    global onTrack
    onTrack += 1
    print("Forwarad" + str(onTrack))
    playAudio(firstTime=False)
    print("Forwarad done" + str(onTrack))

def songBackward():
    global onTrack
    print("Backward" + str(onTrack))
    onTrack -= 1
    print("Backward done" + str(onTrack))
    playAudio(firstTime=False)




#listener_thread = Listener(on_press=on_press, on_release=None)

#listener_thread.start()

root.title("Music Player")
root.geometry("1336x594")



canvas = tk.Canvas(root, bg='darkgray')
canvas.place(relwidth=1, relheight=1)

labelFrame = tk.Frame(canvas, height=100,  width=100, bg='darkgray')
labelFrame.place(relheight=1, relwidth=0.7, relx=0.3)

buttonFrame = tk.Frame(canvas, height=100, width=100, bg='lightgray')
buttonFrame.place(relheight=1, relwidth=0.3)

button1 = tk.Button(buttonFrame, text="Play Queue", command=playAudio)
button1.place(bordermode=tk.OUTSIDE, relheight=0.1, relwidth=0.35, relx=0.3, rely=0.35)

button2 = tk.Button(buttonFrame, text="Pause", command=pauseAudio)
button2.place(bordermode=tk.OUTSIDE, relheight=0.1, relwidth=0.35, relx=0.3, rely=0.5)

addTrack = tk.Button(buttonFrame, text="Add Track", command=addAudio)
addTrack.place(bordermode=tk.OUTSIDE, relheight=0.1, relwidth=0.35, relx=0.3, rely=0.65)

volumeSlider = tk.Scale(buttonFrame, from_=100, to=0, command=setVol, bg='lightgray')
volumeSlider.place(relheight=0.3, relwidth=0.2, relx=0.7, rely=0.4)

volumeSlider.set(100)

loopQueue = tk.Checkbutton(buttonFrame, text="Loop Queue", command=loopQueueCommand, bg='lightgray')
loopQueue.place(relheight=0.02, relwidth=0.3, relx=0.3, rely=0.8)

loopSong = tk.Checkbutton(buttonFrame, text="Loop Song", command=loopSongCommand, bg='lightgray')
loopSong.place(relheight=0.02, relwidth=0.3, relx=0.3, rely=0.9)

shuffle = tk.Checkbutton(buttonFrame, text="Shuffle", command=doShuffleCommand, bg='lightgray')
shuffle.place(relheight=0.02, relwidth=0.3, relx=0.3, rely=0.85)

forwardSong = tk.Button(buttonFrame, text=">>>", command=songForward)
forwardSong.place(bordermode=tk.OUTSIDE, relheight=0.05, relwidth=0.175, relx=0.475, rely=0.22)

backwardSong = tk.Button(buttonFrame, text="<<<", command=songBackward)
backwardSong.place(bordermode=tk.OUTSIDE, relheight=0.05, relwidth=0.175, relx=0.3, rely=0.22)

removeField = tk.Entry(buttonFrame, textvariable=removeEntryText)
removeField.place(relheight=0.03, relwidth=0.25, relx=0.3, rely=0.15)

submitButton = tk.Button(buttonFrame, text="Clear", command=removeSong)
submitButton.place(relheight=0.03, relwidth=0.1, relx=0.55, rely=0.15)

fieldLabel = tk.Label(buttonFrame, text="Song Number To Remove")
fieldLabel.place(relheight=0.03, relwidth=0.35, relx=0.3, rely=0.1)

fileBar = tk.Scrollbar(labelFrame)
fileBar.pack(side=tk.RIGHT, fill=tk.Y)

fileBox = tk.Listbox(labelFrame, bg='darkgray', yscrollcommand=fileBar.set, activestyle='dotbox')
fileBox.place(relheight=1, relwidth=1)
fileBox.bind('<<ListboxSelect>>', setSong)

fileBar.config(command=fileBox.yview)

fastForward = tk.Button(buttonFrame, text=">>", command=fastForwardCommand)
fastForward.place(bordermode=tk.OUTSIDE, relheight=0.05, relwidth=0.175, relx=0.475, rely=0.27)

fastBackward = tk.Button(buttonFrame, text="<<", command=fastBackwardCommand)
fastBackward.place(bordermode=tk.OUTSIDE, relheight=0.05, relwidth=0.175, relx=0.3, rely=0.27)

moveQueue()
root.mainloop()