import pyaudio
import timeserver
import threading
import wave
from multiprocessing import Process


class Recorder():
    def __init__(self, chunk=1024, channels=1, rate=8000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    def start(self):
        threading._start_new_thread(self.__recording, ())
    #开始线程

    def __recording(self):
        #开始录音编码
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while (self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
            # print(self._frames)
            print(data)
            # 这个data就是每秒的时间码

        stream.stop_stream()
        stream.close()
        p.terminate()


    def stop(self):
        self._running = False

    def save(self, filename):
    # 保存文件为wav文件
        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()
        print("Saved Success")

signal = threading.Event()

def timevoice():
    rec = Recorder()
    begin = timeserver.time()
    print("Start recording")
    rec.start()
    signal.wait()
    print("Stop recording")
    rec.stop()
    fina = timeserver.time()
    t = fina - begin
    print('录音时间为%ds' % t)
    rec.save("d:/work/send/one.wav")

