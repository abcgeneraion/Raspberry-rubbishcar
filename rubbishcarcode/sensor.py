import RPi.GPIO as GPIO

class Sensor(object):
    def __init__(self, port):
        self.port = port
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def hear_sound(self):
        return GPIO.input(self.port)==0


if __name__=='__main__':
    sensor = Sensor(17)#BCM编码下的引脚
    while True:
        if sensor.hear_sound():
            print('sound detected')
            break