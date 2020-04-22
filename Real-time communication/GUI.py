from tkinter import *
import tkinter.messagebox
from threading import *
import timeserver
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
import multiprocessing
from voice import *
from server import *
from play import *
from timeserver import *


# 这个作为发送端
root = Tk()
root.maxsize(480, 360)
root.minsize(480, 360)
# 在此界面中大小为（480,360）
# 主要功能，录音，传输

on_hit = False
on_hit2 = False
on_hiton = False
class myThread(threading.Thread):
    # 继承父类threading.Thread

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数

        if (self.threadID == 1):
            voice()
            #录音

        if (self.threadID == 2):
            send()
            #发送

        if (self.threadID == 3):
            play_voice("d:/work/send/one.wav")
            # 播放

        if (self.threadID == 4):
            # 进行实时通信
            # 点击呼叫按钮就是进行实时通讯
            timetovoice()


def play():
    tkinter.messagebox.showinfo('提示', '正在播放')
    global on_hit2
    if on_hit2 == False:
        on_hit2 = True
        var.set('正在播放')

    p = myThread(3, "Thread-3", 3)
    p.start()


def shutdown3():
    signal1.set()
    tkinter.messagebox.showinfo('提示', '结束播放')
    # 提前终止并且完成保存音频文件
    global on_hit2
    if on_hit2 == True:
        on_hit2 = False
        var.set('')


def helloCallBack():
    # 把耗时间长的放到一个thread中使用
    tkinter.messagebox.showinfo('提示', '正在录音!')
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('正在录音')
    v = myThread(1, "Thread-1", 1)
    v.start()


def shutdown():
    signal.set()
    tkinter.messagebox.showinfo('提示', '录音完成')
    # 提前终止并且完成保存音频文件
    global on_hit
    if on_hit == True:
        on_hit = False
        var.set('')

# 用户点击发送,触发send函数
def send_voice():
    tkinter.messagebox.showinfo('提示', '发送录音')
    s = myThread(2, "Thread-2", 2)
    s.start()
# 发送语音


def ontimechat():
    tkinter.messagebox.showinfo('提示', '正在进行通话')
    ON_time = myThread(4, "Thread-4", 4)
    ON_time.start()



def shutdown2():
    tkinter.messagebox.showinfo('提示', '挂断电话')
    signal_timeserver.set()




class Control:

    def __init__(self, master):
        self.master = master
        self.initWidgets()

    def initWidgets(self):

        B = Button(root, text="录音", command=helloCallBack)
        B.place(x=130, y=60, width=100, height=50)

        C = Button(root, text="结束录音", command=shutdown)
        C.place(x=230, y=60, width=100, height=50)

        S = Button(root, text="发送", command=send_voice)
        S.place(x=130, y=180, width=200, height=50)

        T = Button(root, text="实时通话", command=ontimechat)
        T.place(x=130, y=240, width=100, height=50)

        WW = Button(root, text="挂断", command=shutdown2)
        WW.place(x=230, y=240, width=100, height=50)

        q = Button(root, text="播放", command=play)
        q.place(x=130, y=120, width=100, height=50)

        q = Button(root, text="结束播放", command=shutdown3)
        q.place(x=230, y=120, width=100, height=50)


var = StringVar()


ft = tkFont.Font(family='Fixdsys', size= 15, weight=tkFont.BOLD)
ft1 = tkFont.Font(size=15, slant=tkFont.ITALIC)
ft2 = tkFont.Font(size=15, weight=tkFont.BOLD, underline=1, overstrike=1)
# 不同的字体

w = Label(root, text="欢迎使用网络电话-发送端!",font = ft)
w.place(x=115, y=20, width=250, height=30)

w1 = Label(root, textvariable=var,font = ft)
w1.place(x=110, y=300, width=250, height=30)

root.title("网络电话-发送端")
Control(root)
root.mainloop()




