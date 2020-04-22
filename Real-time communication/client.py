import socket
import threading
import sys
import socketserver
import hashlib
from RC4_wen import *
key = "adfnqjwejqijweoiuscnjsdnjk1234189304hidfhiqwuehjioejncjkankjnxajduixqwehiuh3y4r78hbf"

def get():
    # 客户端作为请求接受端
    client = socket.socket()
    client.connect(('localhost', 6666))
    # 客户端完成连接
    # 等待服务端传来的文件
    file_size = client.recv(1024)
    print('服务端检测到文件大小：', int(file_size))
    client.send('可以发送数据了'.encode(encoding='utf-8'))
    file_total_size = int(file_size)
    receive_size = 0

    filename = 'd:/work/get/one.wav.RC4'
    # 保存传输文件地址
    f = open(filename, 'wb')
    m = hashlib.md5()
    while receive_size < file_total_size:
        data = client.recv(1024)
        m.update(data)
        receive_size += len(data)
        f.write(data)
        print(file_total_size, receive_size)
        # 输出传输进度
    else:
        new_file_md5 = m.hexdigest()
        print('数据接收完成！')
        f.close()
        client.send('可以发送md5值了'.encode())
    # 在这个时候添加一个提示。
    serve_md5 = client.recv(1024)
    print('新文件md5:', new_file_md5)
    print('原文件md5:', serve_md5)
    RC4_main(filename, key)
    client.close()

