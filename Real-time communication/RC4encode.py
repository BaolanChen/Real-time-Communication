def init_box(key):
  #S盒
    s_box = list(range(256))
    # 初始化状态向量，256个字节，用来作为密钥流生成的种子1
    j = 0
    for i in range(256):
        j = (j + s_box[i] + ord(key[i % len(key)])) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]#置换
    return s_box
# 由密钥T开始对状态向量S进行置换操作


def ex_encrypt(plain, box, mode):
    res = []
    i = j = 0
    for s in plain:
        # 明文和密钥流长度相同，密文也是
        # 密文第i字节=明文第i字节^密钥流第i字节
        i = (i + 1) % 256
        j = (j + box[i]) % 256
        box[i], box[j] = box[j], box[i]
        t = (box[i] + box[j])% 256
        k = box[t]
        # 这里的K就是当前生成的一个秘钥流中的一位
        res.append(chr(ord(s) ^ k))
        #进行加密，^是异或运算符
    cipher = "".join(res)
    # 将res list形式连起来
    # Python join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
    if  mode == 1:
        # 化成可视字符需要编码
        print("加密后的输出:")
        print(cipher.encode())
        return cipher

    if mode == 2:
        # 化成可视字符需要编码
        print("解密后的输出:")
        print(cipher)
        return cipher

#
# key='123'
# message = 'asdfasdadfasdf////789h/1//jhgkdgfh1//1/1/2/2/3//0//8/'
#
# box = init_box(key)
# x = ex_encrypt(message,box,1)

# box = init_box(key)
# ex_encrypt(x, box, 2)

