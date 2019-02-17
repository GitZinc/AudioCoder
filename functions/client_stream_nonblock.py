import pyaudio
import socket
import time

p = pyaudio.PyAudio()

BUF_SIZE = 512

server_addr = ('192.168.1.2',7777)
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(server_addr)
print("Connected Successfully")
def callback(in_data, frame_count, time_info, status):
    data4 = bytes(0)
    # print(in_data)
    # print(frame_count)
    # print(time_info)
    # print(status)
    for i in range (int(4096/BUF_SIZE)):
        tmp, addr = client.recvfrom(BUF_SIZE)
        data4 = data4 + tmp
        # print('\n'+str(len(data))+'\n')
    # data = input[nowpoint : nowpoint + 4095]
    return(data4, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=8000,
                output=True,
                stream_callback=callback)


stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    # point = point + 4096
    time.sleep(0.1)
# data, addr = client.recvfrom(BUF_SIZE) # buffer size is 1024 bytes

# while data != '':
#     stream.write(data)
#     client.sendto('ok'.encode('utf-8'),addr)#向服务端发送成功通知\
#     data, addr = client.recvfrom(BUF_SIZE) # buffer size is 1024 bytes
stream.stop_stream()
stream.close()

p.terminate()
