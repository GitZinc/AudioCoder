"""PyAudio Example: Play a wave file (callback version)."""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyaudio
import wave
import time

class PlayThread(QThread):
    # 定义信号,定义参数为str类型
    _signal = pyqtSignal(str)
    _infosignal = pyqtSignal(str)
    _endsignal = pyqtSignal(int)
    def __init__(self):
        super(PlayThread, self).__init__()
    def pathset(self,path):
        self.path = path
        print("self.path = " + self.path)
    def setstate(self,state):
        self.state = state

    # def setinfo(self,numframes,format,channels,rate):
    #     self.numframes = numframes
    #     self.format = format
    #     self.channels = channels
    #     self.rate = rate
    #
    # def getinfo(self):
    #     return(self.numframes,self.format,self.channels,self,rate)


    def run(self):
        print("Playing...")
        # self.path = "output.wav"
        wf = wave.open(self.path, 'rb')
        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()
        global nowframes
        nowframes = 0
        # define callback (2)
        def callback(in_data, frame_count, time_info, status):
            # print("Frames_count = "+ str(frame_count))
            global nowframes
            nowframes += frame_count
            self._signal.emit(str(nowframes / self.mynumframes))
            data = wf.readframes(frame_count)

            return (data, pyaudio.paContinue)

        self.mynumframes = wf.getnframes()
        self.myformat=p.get_format_from_width(wf.getsampwidth())
        self.mychannels = wf.getnchannels()
        self.myrate = wf.getframerate()

        self._infosignal.emit("总帧数: " + str(self.mynumframes) + "\n文件格式: " + str(self.myformat) + "\n通道数: " + str(self.mychannels) + "\n帧率: " + str(self.myrate))

        # self.setinfo(self.mynumframes,self.myformat,self.mychannels,self.myrate)
        # print(self.mynumframes)
        # print(self.myformat)
        # print(self.mychannels)
        # print(self.myrate)
        # open stream using callback (3)
        stream = p.open(format=self.myformat,
                        channels=self.mychannels,
                        rate=self.myrate,
                        output=True,
                        stream_callback=callback)

# open stream (2)
# stream = p.open(format=p.get_format_from_width(2),
#                 channels=2,
#                 rate=44100,
#                 output=True)

        # start the stream (4)
        print("start stream.")
        stream.start_stream()

        # wait for stream to finish (5)
        while ((self.state) & (stream.is_active())):
            time.sleep(0.1)

        # stop stream (6)
        stream.stop_stream()
        stream.close()
        wf.close()

        # close PyAudio (7)
        p.terminate()
        self._endsignal.emit(0)
if __name__ == '__main__':
    PT = PlayThread()
    PT.pathset("output.wav")
    # print(PT.path)
    PT.start()