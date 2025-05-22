from tkinter import *
from tkinter import filedialog
from playsound3 import playsound
from mutagen.mp3 import MP3
from datetime import datetime

queue = {}

def deletesong():
    global queue
    global deletee
    numb= int(deletee.get())
    queue.pop(list(queue.keys())[numb-1])

def timenow():
    global sound
    global filelist
    global queue
    data = datetime.strftime(datetime.now(),"%H%M%S")
    currtime= int(data[0:2])*3600+int(data[2:4])*60+int(data[4:])
    try:
        if currtime in list(queue.keys()):
            sound=playsound(str(queue[currtime][1]),block=False)
    except:
        pass
    currqueue = []
    queue = dict(sorted(queue.items(), key=lambda x: x[0]))
    numb = 1
    for secs,path,time in queue.values():
        currqueue.append(f"{numb} : {path} {time}")
        numb+=1
    try:
        filelist.destroy()
    except:
        pass
    filelist = Label(tk,text=("\n".join(currqueue)))
    filelist.grid(row=8,column=0,rowspan=10,columnspan=3)
    tk.after(1000,timenow)
def search():
    global filesearch
    filesearch = filedialog.askopenfilename()
    return filesearch
def stopfunc():
    global sound
    sound.stop()
def save():
    global musictimem
    global musictimeh
    global filesearch
    global queue
    h=int(musictimeh.get())
    m = int(musictimem.get())
    try:
        s = int(musictimes.get())
    except ValueError:
        s = 0
    beginning = h*3600+m*60+s
    end= beginning + round(MP3(filesearch).info.length)
    if h >=0 and h <= 24 and m >=0 and m <=60 and s>=0 and s<=60:
        taken=False
        for keys,values in queue.items():
            if len(list(set(range(beginning,end+1)) & set(range(keys,values[0]+1)))) != 0:
                error.config(text="There's already a song playing in that timeframe! Please choose another time!")
                taken = True
        if not taken:
            if m <10:
                m = f"0{m}"
            if s <10:
                s=f"0{s}"
            queue[beginning] = [end,filesearch,f"{h}:{m}:{s}"]
    else:
        error.config(text="That's not an acceptable time. Please choose another one.")
        
tk = Tk()
tk.title("MP3 player")
tk.geometry("600x600")


musiclabel = Label(tk, text="MP3 file: ")
musiclabel.grid(row=1,column=0)

musicbutton = Button(tk,command=search,text="Locate")
musicbutton.grid(row=1,column=1)

musictimehlabel = Label(tk, text="Hour: ")
musictimehlabel.grid(row=2,column=0)

musictimeh = Entry(tk)
musictimeh.grid(row=2,column=1)

musictimemlabel = Label(tk, text="Minutes: ")
musictimemlabel.grid(row=3,column=0)

musictimem = Entry(tk)
musictimem.grid(row=3,column=1)

musictimeslabel = Label(tk, text="Seconds: (defaults to 00 if not given)")
musictimeslabel.grid(row=4, column=0)

musictimes = Entry(tk)
musictimes.grid(row=4,column=1)

stop= Button(tk,text="Stop",command=stopfunc)
stop.grid(row=5,column=0)

okay = Button(tk, text="Save", command=save)
okay.grid(row=5,column=1)

deletee = Entry(tk)
deletee.grid(row=5, column=2)

deleteb = Button(tk, command=deletesong,text="Delete")
deleteb.grid(row=5, column=3)

error = Label(tk)
error.grid(row=6,column=0,columnspan=2)

queuet = Label(tk, text="Queue of MP3 files")
queuet.grid(row=7,column=0,columnspan=2)

tk.after(1000,timenow)
tk.mainloop()