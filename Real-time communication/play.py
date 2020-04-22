#播放音频
import wave
from pyaudio import *
from pyaudio import PyAudio, paInt16
import threading
signal1 = threading.Event()

def play_voice(audio_file):

    chunk = 1024  # 2014kb
    wf = wave.open(audio_file, 'rb')
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)

    data = wf.readframes(chunk)  # 读取数据

    while True:
        data = wf.readframes(chunk)
        if signal1.is_set():
            # 点击结束后这个变为true
            break
        if data == "":
            break
        stream.write(data)

    stream.stop_stream()  # 停止数据流
    stream.close()
    p.terminate()  # 关闭 PyAudio
    print('play函数结束！')


