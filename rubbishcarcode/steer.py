import RPi.GPIO as GPIO
import time

class Steer(object):
    def __init__(self, string):
        if string=='可回收物':
            self.port = 6
        elif string=='有害垃圾':
            self.port = 13
        elif string=='厨余垃圾':
            self.port = 19
        elif string=='其他垃圾':
            self.port = 26
            
        print(self.port)
            
        self.fpWM = 50  # 50 Hz
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port, GPIO.OUT)
        self.gear = GPIO.PWM(self.port,self.fpWM)
        # .start(dc) dc代表占空比（范围：0.0 <= dc >= 100.0）
        self.gear.start(0)

    def set_degree(self,degree):
        #此公式计算出舵机旋转角度所对应的脉宽调制电路的占空比
        duty = float(degree)/18 + 2.5
        #改变占空比
        self.gear.ChangeDutyCycle(duty)
        time.sleep(0.5)

    def open(self):
        print('open')
        self.set_degree(90)

    def close(self):
        print('close')
        self.set_degree(0)



if __name__=="__main__":    # 模块测试
    lid=Steer('其他垃圾')
    time.sleep(2)
    lid.open()
    time.sleep(5)
    lid.close()
    GPIO.cleanup()