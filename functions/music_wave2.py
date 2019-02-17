# %matplotlib inline
import wave
import struct
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
import pyaudio

class MyMusicWave():
    """docstring for My"""
    # x_display:显示的播放长度,单位为秒 update_frame:每次更新的frame数量,值约小越流畅
    def __init__(self, filename , x_display = 1 , update_frame = 100):
        # 读取wav文件
        self.filename = filename
        self.wavefile = wave.open(self.filename, 'r')  # open for writing

        # 读取wav文件的四种信息的函数。期中numframes表示一共读取了几个frames。
        self.nchannels = self.wavefile.getnchannels()
        self.sample_width = self.wavefile.getsampwidth()
        self.framerate = self.wavefile.getframerate()
        self.numframes = self.wavefile.getnframes()

        print("channel", self.nchannels)
        print("sample_width", self.sample_width)
        print("framerate", self.framerate)
        print("numframes", self.numframes)


        # channel 1
        # sample_width 2
        # framerate 16000
        # numframes 22720
        self.x_display = x_display
        self.update_frame = update_frame

    def save_frame(self):
        # 建一个y的数列，用来保存后面读的每个frame的amplitude。
        self.y = np.zeros(self.numframes)
        # for循环，readframe(1)每次读一个frame，取其前两位，是左声道的信息。右声道就是后两位啦。
        # unpack是struct里的一个函数，用法详见http://docs.python.org/library/struct.html。
        # 简单说来就是把＃packed的string转换成原来的数据，无论是什么样的数据都返回一个tuple。这里返回的是长度为一的一个
        # tuple，所以我们取它的第零位。
        for i in range(self.numframes):
            val = self.wavefile.readframes(1)
            left = val[0:2]
            # right = val[2:4]
            v = struct.unpack('h', left)[0] # 'h' represent for short integer 2字节
            self.y[i] = v
        # framerate就是声音的采用率，文件初读取的值。
        Fs = self.framerate
        self.Ts = 1.0 / self.framerate
        # time = np.arange(0, numframes) * Ts
        time = self.numframes * self.Ts
        # 显示时域图(波形图)

        self.fig,ax = plt.subplots()
        x = np.arange(0, self.x_display, self.Ts)
        self.line, = ax.plot(x, self.y[0:int(self.x_display/self.Ts)])    # ','选择列表的第一位

    # 有优化空间
    def animate(self,i):
        self.line.set_ydata(self.y[0 + self.update_frame*i : int(self.x_display/self.Ts) + self.update_frame*i]) # 更新ydata
        return self.line,

    def init(self):
        self.line.set_ydata(self.y[0:int(self.x_display/self.Ts)]) # 更新ydata
        return self.line,

    def plotwave(self):
        # interval 更新频率, blit 是否更新没变的数据
        interval = self.x_display*1000/(self.framerate/self.update_frame)
        ani = animation.FuncAnimation(fig = self.fig, func = self.animate, frames = self.numframes, init_func = self.init, interval = interval, blit = False)

        # 此处将生成的动态图片存为gif
        # ani.save('phantom.gif', writer='imagemagick', fps=30)
        plt.title('Wave')
        plt.xlabel('Time/Second')
        plt.ylabel('Amplitude')
        plt.show()

if __name__ == '__main__':
    filename = 'output.wav'
    x_display = 1
    update_frame = 100
    mywave = MyMusicWave(filename,x_display,update_frame)
    mywave.save_frame()
    mywave.plotwave()