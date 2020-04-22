# 在此模块中进行调用麦克风进行获取声音
# 进行网络电话的网络安全课设
import socket
import numpy as np
import pyaudio
import wave
from pyaudio import PyAudio, paInt16
import os
import timeserver


# 1） 利用系统麦克风，获取模拟语音，经过AMR压缩编码后，对码流进行RC4加密，通过网络进行传输；
# 2） 接收端接收到码流后先进行解密，再进行AMR解码，并播放语音。


class recoder:
    NUM_SAMPLES = 2000
    # pyaudio内置缓冲大小
    SAMPLING_RATE = 8000
    # 取样频率
    LEVEL = 500
    # 声音保存的阈值
    COUNT_NUM = 20
    # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 8
    # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
    TIME_COUNT = 20
    # 录音时间，单位s
    Voice_String = []
    # 保存音频信息
    _running = True


# 录音
    def recoder(self):
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE, input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []
        time_count = self.TIME_COUNT
        # 此为录音时间

        while(self._running):
            time_count -= 1
            # print time_count
            # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            large_sample_count = np.sum( audio_data > self.LEVEL )
            print(time_count, np.max(audio_data))
            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH
            else:
                save_count -= 1

            if save_count < 0:
                save_count = 0

            if save_count > 0 :
            # 将要保存的数据存放到save_buffer中
                #print  save_count > 0 and time_count >0
                save_buffer.append( string_audio_data )
            else:
            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                if len(save_buffer) > 0 :
                    self.Voice_String = save_buffer
                    print(save_buffer)
                    print("Recode a piece of  voice successfully!")
                    return True
            if time_count == 0:
                if len(save_buffer)>0:
                    self.Voice_String = save_buffer
                    # 将得到的声音进行保存
                    print(save_buffer)
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False

    # 保存到.wav文件中
    def savewav(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes(np.array(self.Voice_String).tostring())
        wf.close()
        print("save voice.wav successfully!")

    def stop(self):
        self._running = False



def get_voice():
    r = recoder()
    r.recoder()
    r.savewav("D:/voice/test.wav")

def save_voice():
    r = recoder()
    r.stop()
    r.savewav("D:/voice/test.wav")

# get_voice()


def wav_to_pcm(wav_file):
    # 假设 wav_file = "音频文件.wav"
    # wav_file.split(".") 得到["音频文件","wav"] 拿出第一个结果"音频文件"  与 ".pcm" 拼接 等到结果 "音频文件.pcm"
    pcm_file = "%s.pcm" %(wav_file.split(".")[0])

    # 就是此前我们在cmd窗口中输入命令,这里面就是在让Python帮我们在cmd中执行命令
    os.system("ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s"%(wav_file,pcm_file))

    return pcm_file
