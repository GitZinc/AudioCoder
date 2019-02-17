"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""
import pyaudio
import wave
import time
import socket
import threading
from PyQt5 import QtGui
from PyQt5.QtCore import *



class UdpThread(QThread):
    def __init__(self):
        super(UdpThread, self).__init__()
    def run(self):
        BUF_SIZE = 1024
        MAX_RECORD_SECONDS = 5
        server_addr = ('192.168.1.2',7777)
        client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client.bind(server_addr)
        print("Connected Successfully")
        WAVE_OUTPUT_FILENAME = 'udp.wav'
        CHUNK = BUF_SIZE/8
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 8000

        print("* recording")
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(RATE)

        # for i in range(0, int(RATE / CHUNK * MAX_RECORD_SECONDS)):
        #     data = stream.read(CHUNK)
        #     frames.append(data)

        # while (self.state)&(i <= int(RATE / CHUNK * MAX_RECORD_SECONDS)):
            # print("self.state = " + str(self.state))
        i = 0
        for i in range(0, int(RATE / CHUNK * MAX_RECORD_SECONDS)):
            name='thread'+str(i)
            locals()['thread'+str(i)]=binsave(client,BUF_SIZE,wf,server_addr)
            locals()['thread'+str(i)].start()
            locals()['thread'+str(i)].join()
            i = i + 1
        # while self.state():
        #     data = stream.read(CHUNK)
        #     frames.append(data)
        wf.close()

        print("* done recording")

class binsave (threading.Thread):
    def __init__(self,client,BUF_SIZE,wavefile,server_addr):
        threading.Thread.__init__(self)
        # self.data = data
        self.client = client
        self.BUF_SIZE = BUF_SIZE
        self.wf = wavefile
        self.server_addr = server_addr
    def run(self):
        data,addr = self.client.recvfrom(self.BUF_SIZE)
        print ("开始线程：" + self.name)
        self.wf.writeframes(data)
        print(len(data))
        print ("退出线程：" + self.name)
