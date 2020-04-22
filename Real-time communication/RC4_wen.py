import base64
import os
import struct
import binascii
# 对amr文件进行加密
# 对文件进行加密

def RC4(pkey, keylen, pin, dlen):
    N = 65536#256*256
    S = list(range(N))
    j = 0
    for i in range(N):
        j = (j + S[i] + pkey[i % keylen]) % N
        temp = S[i]
        S[i] = S[j]
        S[j] = temp
    i = j = 0
    pout = b''
    for x in range(dlen):
        i = i + 1
        j = (j + S[i]) % N
        temp = S[i]
        S[i] = S[j]
        S[j] = temp
        pout += struct.pack('H', pin[x] ^ S[(S[i] + S[j]) % N])
    return (pout)


# bytes->short
def Coding(data):
    if (len(data) % 2):
        # 如果是奇数就加上0
        data += b'\0'
    dlen = len(data) // 2
    return (struct.unpack(str(dlen) + 'H', data))
# 按照指定格式将Python数据转换为字符串,该字符串为字节流

# short->bytes
def unCoding(data):
    d = b''
    for i in range(len(data)):
        d += struct.pack('H', data[i])
    return (d)


# 产生32字节密钥
def CreatKey(Keyt):
    pl = len(Keyt)
    Key = b''
    r = 0
    for i in range(32):
        k = (Keyt[r % pl] + i) % 256
        Key += struct.pack('B', k)
        r += 1
    return Key


# 更新密钥
def UpdataKey(Keyt):
    Key = unCoding(Keyt)
    # 循环左移
    Key = Key[1:] + struct.pack('B', Key[0])
    tem = 0
    # 求和
    for i in range(len(Key)):
        tem += Key[i];
    Keyo = b''
    # Xor
    for i in range(len(Key)):
        Keyo += struct.pack('B', (Key[i] ^ tem) % 256)
        tem += Keyo[i] >> 3
        tem = tem % 256
    return (Coding(Keyo))


def RC4_main(filename,key):
    # 获得输入文件
    try:
        fin = open(filename, 'rb')
    except:
        print('打开文件失败！')
    print(filename)
    # 打开输出文件
    if filename[-4:] == '.RC4':
        eID = 1
        key = key.encode()
        ofilename = filename[:-4]
    else:
        eID = 2
        # key = input('输入加密密钥: ').encode()
        key = key.encode()
        ofilename = filename + '.RC4'
    key = Coding(CreatKey(key))
    key = UpdataKey(key)

    fout = open(ofilename, 'wb')
    print(ofilename)
    # 解密
    if eID == 1:
        # 读文件长度
        filelen = struct.unpack('I', fin.read(4))[0]
        print('FlieLen =', filelen, '\n......')
        while 1:
            ps = fin.read(2)
            if not ps:
                break
            packsize = struct.unpack('H', ps)[0]
            # 读数据
            dd = fin.read(packsize)
            # 解密
            dd = Coding(dd)
            x = RC4(key, len(key), dd, len(dd))
            key = UpdataKey(key)
            # crc
            crc = struct.unpack('I', fin.read(4))[0]
            if binascii.crc32(x) != crc:
                print('CRC32校验错误！', crc, binascii.crc32(x))
            fout.write(x)
        # 裁剪末尾填充位
        fout.truncate(filelen)
    # 加密
    elif eID == 2:
        # 获得文件长度
        fin.seek(0, 2)
        filelen = fin.tell()
        print('FlieLen =', filelen, '\n......')
        fin.seek(0, 0)
        fout.write(struct.pack('I', filelen))
        while 1:
            # 读数据
            dd = fin.read(65534)
            if not dd:
                # 文件结束
                break
            # 末尾填充
            srl = len(dd)
            if srl % 2:
                srl += 1;
                dd += b'\0'
            # crc
            crc = struct.pack('I', binascii.crc32(dd))
            # 加密数据
            dd = Coding(dd)
            x = RC4(key, len(key), dd, len(dd))
            key = UpdataKey(key)
            # 写入文件
            fout.write(struct.pack('H', srl))
            fout.write(x)
            fout.write(crc)
    fin.close()
    fout.close()
    print('encode success')


# filename = "d:/work/get/one.wav"
# # filename = "d:/work/send/one.wav"
#
#
# key = "adfnqjwejqijweoiuscnjsdnjk1234189304hidfhiqwuehjioejncjkankjnxajduixqwehiuh3y4r78hbf"
# RC4_main(filename,key)

