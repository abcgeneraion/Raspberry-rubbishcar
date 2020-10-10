import RPi.GPIO as GPIO
import time

class Lamp(object):
    #__init__方法是类的构造函数，调用类的方法时此方法会自动执行
    def __init__(self, port):
        self.port = port
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port, GPIO.OUT)
        self.on_state = GPIO.HIGH
        self.off_state = not self.on_state

    def set_on(self):
        GPIO.output(self.port, self.on_state)

    def set_off(self):
        GPIO.output(self.port, self.off_state)

    def is_on(self):
        return GPIO.input(self.port) == self.on_state

    def is_off(self):
        return GPIO.input(self.port) == self.off_state

    def toggle(self):
        if self.is_on():
            self.set_off()
        else:
            self.set_on()

    def blink(self, t=0.3):
        self.set_off()
        self.set_on()
        time.sleep(t)
        self.set_off()


if __name__=='__main__':
    led1 = Light(26)
    led1.blink()
    led2 = Light(19)
    led2.blink()
    #  在任何程序结束后，请养成清理用过的资源的好习惯。使用 RPi.GPIO 也同样需要这样。恢复所有使用过的通道状态为输入，
    #  您可以避免由于短路意外损坏 Raspberry Pi 针脚。注意，该操作仅会清理您的脚本使用过的 GPIO 通道。
    GPIO.cleanup()
