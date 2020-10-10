import snowboydecoder
import signal

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True
#当 signal.signal(signal.SIGTERM, handler)监听过程中，
#捕获到信号signal.SIGTERM时,就会去执行handler函数
#而handler函数中一般都有全局变量，进程或线程通过此全局变量就可以知道该如何执行
#handler方法的两个参数分别是 信号编号, 程序帧
def interrupt_callback():
    global interrupted
    return interrupted


model = './audiofile/你好，大头鱼.pmdl'  #唤醒词

signal.signal(signal.SIGINT, signal_handler)
#在signal模块中，主要是使用signal.signal()函数来预设信号处理函数



detector = snowboydecoder.HotwordDetector(model, sensitivity=0.6)#调用构造方法

def temp_func():
    print('aaa')
    detector.terminate() # 结束监控热词    
    snowboydecoder.play_audio_file() # ding一声

if __name__=='__main__':    # 模块测试
    
    print('Listening... Press Ctrl+C to exit')

    detector.start(detected_callback=temp_func,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)
    print('over')
    detector.terminate()
