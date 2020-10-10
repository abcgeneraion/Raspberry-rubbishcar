#!/usr/bin/python
#coding: utf8
import sys
import RPi.GPIO as GPIO
import time
import sys
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.options import define,options
from steer import Steer

define("port",default=8000,type=int)
IN1 = 12
IN2 = 16
IN3 = 20
IN4 = 21
def init():
        #采取BCM编码方式
        GPIO.setmode(GPIO.BCM)
        # 将引脚设置为输入模式
        GPIO.setup(IN1,GPIO.OUT)
        GPIO.setup(IN2,GPIO.OUT)
        GPIO.setup(IN3,GPIO.OUT)
        GPIO.setup(IN4,GPIO.OUT)

# 前进
def forward(tf):
        print("前进")
        GPIO.output(IN1,GPIO.HIGH)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.HIGH)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 后退
def reverse(tf):
        print("后退")
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.HIGH)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.HIGH)
        time.sleep(tf)
        GPIO.cleanup()

# 左转弯
def left(tf):
        print("左转弯")
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.HIGH)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 右转弯
def right(tf):
        print("右转弯")
        GPIO.output(IN1,GPIO.HIGH)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 后左转弯
def pivot_left(tf):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.HIGH)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 后右转弯
def pivot_right(tf):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.HIGH)
        time.sleep(tf)
        GPIO.cleanup()

# 原地左转
def p_left(tf):
        GPIO.output(IN1,GPIO.LOW)
        GPIO.output(IN2,GPIO.HIGH)
        GPIO.output(IN3,GPIO.HIGH)
        GPIO.output(IN4,GPIO.LOW)
        time.sleep(tf)
        GPIO.cleanup()

# 原地右转
def p_right(tf):
        GPIO.output(IN1,GPIO.HIGH)
        GPIO.output(IN2,GPIO.LOW)
        GPIO.output(IN3,GPIO.LOW)
        GPIO.output(IN4,GPIO.HIGH)
        time.sleep(tf)
        GPIO.cleanup()

class IndexHandler(tornado.web.RequestHandler):
        def get(self):
                self.render("index.html")
        def post(self):
                init()
                sleep_time = 0.1
                #1.使用get_argument获取url query参数
                arg = self.get_argument('k')
                if(arg=='w'):
                        forward(sleep_time)
                elif(arg=='s'):
                        reverse(sleep_time)
                elif(arg=='a'):
                        left(sleep_time)
                elif(arg=='d'):
                        right(sleep_time)
                elif(arg=='q'):
                        pivot_left(sleep_time)
                elif(arg=='e'):
                        pivot_right(sleep_time)
                elif(arg=='z'):
                        p_left(sleep_time)
                elif(arg=='x'):
                        p_right(sleep_time)
                elif(arg=='u'or arg=='i' or arg =='o' or arg == 'p'):
                        result = {'u':"可回收物",'i':"厨余垃圾",'o':"有害垃圾",'p':"其他垃圾"}
                        p = result[arg]
                        lid = Steer(p)
                        lid.open()
                        time.sleep(5)  # 打开5秒
                        lid.close()
                else:
                        return False
                self.write(arg)#向前端返回信息

if __name__ == '__main__':

        #以上就是一个简单的web服务，通过访问该 ip 的8000端口 就能访问到设置的相关信息或界面！
        tornado.options.parse_command_line()
        #类 IndexHandler 是一个句柄：描述控制器操作过程的一个动作
        app = tornado.web.Application(handlers=[(r"/",IndexHandler)])
        #通过 tornado.httpserver.HTTPServer 绑定 Application 对象
        http_server = tornado.httpserver.HTTPServer(app)
        #通过 tornado.httpserver.HTTPServer().listen() 设置监听端口
        http_server.listen(options.port)
        #通过 tornado.ioloop.IOLoop.current().start() 开始循环监听端口
        tornado.ioloop.IOLoop.instance().start()





