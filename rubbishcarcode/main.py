import wakeup
from lamp import Lamp
from steer import Steer
import iFlytekVoiceTrans
import baiduvoice
import sizhiAI
import userrecord
import classify

import urllib3
import time


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)# 忽略百度api连接时的报错信息。

led1 = Lamp(26) # LED灯1,录音时亮
led2 = Lamp(19) # LED灯2,AI处理时亮

def ai_work():
    
    wakeup.detector.terminate() # 结束监控热词
    
    wakeup.snowboydecoder.play_audio_file() # ding一声
    led1.set_on()    # 开灯


    # 1.录 用户语音
    state =userrecord.record()
    if state == False:   # 唤醒后太久没说话
        led1.set_off()
        return
    led1.set_off()
    
        
    led2.set_on()
    # 2.用户语音 转 文字
    ai_text = "你说什么"
    user_text = iFlytekVoiceTrans.get_usertext() # 获得语音的文字结果
    #user_text = duvoice.speech_to_text()

    
    # 3.获得 AI文字
    if user_text=='':   # 录音结果有误
        print("AI说: " + ai_text)
        baiduvoice.text_to_speech(ai_text)
    else:                   # 结果无误
        result = classify.get_type(user_text)  # 从话中提取垃圾种类
        
        if result==False:   # 没有说任何垃圾
            ai_text = aibrain.ai_think(user_text)   # 思知机器人回答
            # 4.AI文字 转 语音
            baiduvoice.text_to_speech(ai_text)
        else:
            if result[0] != None:
                print(result[0] + '是' + result[1])
                ai_text = result[0] + '是' + result[1]+','+result[1]+'箱已打开'# 回答xx是xx垃圾
            else:
                print(result[1] + "箱已打开")
                ai_text = result[1]+'箱已打开'
            # 4.AI文字 转 语音
            baiduvoice.text_to_speech(ai_text)
            lid = Steer(result[1])    # 垃圾种类对应的盖子
            lid.open()
            time.sleep(5)  # 打开5秒
            lid.close()

    led2.set_off()   # 关灯

    

if __name__=='__main__':
    
    while True:
        
        print('Sleeping... ')
        
        # 实时监控
        wakeup.detector.start(detected_callback=ai_work,  # 自定义回调函数
                                interrupt_check=wakeup.interrupt_callback,
                                sleep_time=0.03)
        
        #wakeuptool.detector.terminate() # 结束监控热词
        
        print('Sleep again... ')
