import socket
import os
import hashlib
import pyaudio
import time
import threading
import wave
from multiprocessing import Process
import RC4encode

# server 向client发送文件
# 可以使用多线程然后将它进行结束关闭
# 任务是进行实时录音，且同时完成对client的传输
key = "cbl"
# 先实现传输，再实现加密
# 直接实现音频的在线传输
# 之后才是界面按钮

# 1、完成音频传输 ok
# 2、实现加密
class Recorder():
    def __init__(self, chunk=1024, channels=1, rate=8000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True

    def start(self):
        threading._start_new_thread(self.__recording, ())
    #开始线程

    def __recording(self):
        #开始录音编码
        self._running = True
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        server = socket.socket()
        server.bind(('localhost', 6969))
        server.listen(5)
        print("等待客户端连接，发送信息")
        conn, addr = server.accept()

        # 完成连接
        print(conn,addr)
        while (self._running):
            data = stream.read(self.CHUNK)
            conn.send(data)
            print(data)
            # print(ciper.encode())
            # 意思就是不能实现循环

        server.close()

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self._running = False
    # 这里的信号也得传送到client里



signal_timeserver = threading.Event()
# 这里的锁也只能管道自己的传输
def timetovoice():
    rec = Recorder()
    print("Start recording")
    rec.start()
    signal_timeserver.wait()
    print("Stop recording")
    rec.stop()


