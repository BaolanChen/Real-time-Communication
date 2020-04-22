from tkinter import *
import tkinter.messagebox
from get_voice import *
from threading import *
import timeserver
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
from play import *
from client import *
from timeclient import *
import inspect
import ctypes
root = Tk()
root.maxsize(480, 300)
root.minsize(480, 300)
# 在此界面中大小为（480,300）

# 这个作为接受端
class myThread(Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        if self.threadID == 1:
            play_voice('d:/work/get/one.wav')
        if self.threadID == 2:
            get()
        if self.threadID == 3:
            playvoice()

def play():
    tkinter.messagebox.showinfo('提示', '正在播放')
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('正在播放')

    p = myThread(1, "Thread-1", 1)
    p.start()

def play2():
    tkinter.messagebox.showinfo('提示', '已经接收')
    get = myThread(2, "Thread-2", 2)
    get.start()


def shutdown():
    signal1.set()
    tkinter.messagebox.showinfo('提示', '结束播放')
    # 提前终止并且完成保存音频文件
    global on_hit
    if on_hit == True:
        on_hit = False
        var.set('')


def shutdown2():
    tkinter.messagebox.showinfo('提示', '挂断电话')
    signal_time.set()


def ontimechat():
    tkinter.messagebox.showinfo('提示', '正在进行实时通话')
    ontimechat = myThread(3, "Thread-3", 3)
    ontimechat.start()



class Control:

    def __init__(self, master):
        self.master = master
        self.initWidgets()

    def initWidgets(self):
        G = Button(root, text="接收", command=play2)
        G.place(x=130, y=60, width=100, height=50)
        G2 = Button(root, text="播放", command=play)
        G2.place(x=230, y=60, width=100, height=50)
        C = Button(root, text="结束播放", command=shutdown)
        C.place(x=130, y=120, width=200, height=50)

        WW = Button(root, text="接听实时通话", command=ontimechat)
        WW.place(x=130, y=180, width=100, height=50)

        W = Button(root, text="挂断", command=shutdown2)
        W.place(x=230, y=180, width=100, height=50)


var = StringVar()
on_hit = False
ft = tkFont.Font(family='Fixdsys', size= 15, weight=tkFont.BOLD)
ft1 = tkFont.Font(size=15, slant=tkFont.ITALIC)
ft2 = tkFont.Font(size=15, weight=tkFont.BOLD, underline=1, overstrike=1)
# 不同的字体

w1 = Label(root, textvariable=var,font = ft)
w1.place(x=110, y=240, width=250, height=30)

w = Label(root, text="欢迎使用网络电话-接听端!",font = ft1)
w.place(x=115, y=20, width=250, height=30)
root.title("网络电话-接听端")
Control(root)
root.mainloop()

