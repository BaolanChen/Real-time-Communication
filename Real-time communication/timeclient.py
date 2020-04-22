import socket
import threading
import sys
import socketserver
import hashlib
import wave
import pyaudio
from pyaudio import PyAudio, paInt16
import RC4encode


key = "cbl"

signal_time = threading.Event()

# 接收音频信号
# 对信号实现播放
# 设置信号按钮，在双方一个点击结束就会进行结束

def playvoice():
    # chunk = 1024  # 2014kb
    # wf是打开的音频文件
    p = PyAudio()
    # chunk = 1024, channels = 1, rate = 8000
    stream = p.open(format=pyaudio.paInt16, channels=1,
                    rate=8000, output=True)
    # 定义一个数据流对象，帧会直接通过它进行播放
    # 客户端作为请求接受端
    client = socket.socket()
    client.connect(('localhost', 6969))
    # 客户端完成连接
    # 等待服务端传来的文件
    while not signal_time.is_set():
        # 对了如果是对的才是True
        # 这里得设一个挂断信号，这个挂断信号只是自己的，还得有对面的。
        data = client.recv(1024)
        stream.write(data)
        print(data)
        if data == b'':
            break
        # 还得确定一个结束的信号
        # 接收信号，之后进行播放
    client.close()
    # 结束关闭
    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()
    # 关闭 PyAudio


