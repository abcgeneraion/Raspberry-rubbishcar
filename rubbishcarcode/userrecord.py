import pyaudio
import wave
import os
import sys
import time
#from light import Light
from sensor import Sensor

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10     # 最多60秒
WAVE_OUTPUT_FILENAME = "./assets/usersay.wav"    # 文件名


#led = Light(18)
mysensor = Sensor(17)#实例化一个sensor对象


def wait_sound():
    
    no_sound_time_begin = time.time()#返回当前时间戳
    sound_time_begin = 0
    
    while True:     # 等待有效声音

        if mysensor.hear_sound():    # 听到声音
            
            if sound_time_begin==0: # 第一次听到声音
                sound_time_begin = time.time()
                
            else:
                this_time=time.time()
                duration = this_time-sound_time_begin   # 声音持续时间
                if duration<0.1:    # 时间过短，无效
                    sound_time_begin = this_time
                else:   # 有效，开始录音
                    return True
                    
        if time.time()-no_sound_time_begin > 60: # 等待超过1分钟
            return False



def record():
    
    #os.close(sys.stderr.fileno())   # 隐藏错误消息，因为会有一堆ALSA和JACK错误消息，但其实能正常录音

    if wait_sound()==False: # 等待超时
        return False
    
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []


    no_sound_time_begin = 0

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  # 最多60秒
        data = stream.read(CHUNK)
        frames.append(data)
        
        # 判断空气是否安静很久
        if not mysensor.hear_sound():    # 没声音了
            
            if no_sound_time_begin==0: # 第一次没声音
                no_sound_time_begin = time.time()
                
            else:
                this_time=time.time()
                duration = this_time-no_sound_time_begin   # 安静持续时间
                if duration<2:    # 时间过短，无效
                    no_sound_time_begin = this_time
                else:   # 有效，结束录音
                    break
            

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return True


if __name__=='__main__':    # 模块测试
    record()
    
