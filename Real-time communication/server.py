import socket
import os
import hashlib
from RC4_wen import *
# server 向client发送文件
# 可以使用多线程然后将它进行结束关闭

key = "adfnqjwejqijweoiuscnjsdnjk1234189304hidfhiqwuehjioejncjkankjnxajduixqwehiuh3y4r78hbf"
def send():
    # 服务端作为发送端
    server = socket.socket()
    server.bind(('localhost', 6666))
    server.listen(5)
    print("等待客户端连接，发送信息")

    conn, addr = server.accept()
    # 完成连接
    # 在这里添加，可以发送的信息
    filename = "d:/work/send/one.wav"
    RC4_main(filename, key)
    # 这里是录音缓存路径
    filename = filename + ".RC4"

    if os.path.isfile(filename):
        # 判断文件是否存在
        f = open(filename, 'rb')
        # 打开文件
        m = hashlib.md5()
        # hashlib是一个提供字符加密功能的模块，包含MD5和SHA的加密算法
        file_size = os.stat(filename).st_size
        print(file_size)
        conn.send(str(file_size).encode())
        # 给客户端发送文件大小
        conn.recv(1024)
        # 等待并接受客户端的确认，这一步可以解决粘包问题

        for line in f:
            # 边读边循环发送文件
            # 那这里也可以用于实时录音进行amr编码，rc4加密，传送
            m.update(line)
            # 得出每一句的md5值
            conn.send(line)
            # 发送给客户端
        print('file md5:', m.hexdigest())

        f.close()
        conn.recv(1024)
        # 接受客户端的信息
        conn.send(m.hexdigest().encode())

        print('传送完成！')
        # 结束的时候给一个提示

    server.close()
