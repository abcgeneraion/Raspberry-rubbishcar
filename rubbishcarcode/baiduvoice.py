# -*- coding: utf-8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")
import json
import os
from aip import AipSpeech


# 百度语音 API
APP_ID = '22636005'
API_KEY = 'GOECuSrMyCnP5YBiVSy4v3oY'
SECRET_KEY = 'cx6aKMyGcEtk1XSAlYAD4cFhwlsav88n'
    
client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)



# 语音转文字
def speech_to_text():
    
    with open('./audiofile/usersay.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,
    })
    print(result)

    if result["err_no"]==0: #成功返回
        user_text = result["result"][0]
        print("我说: " + user_text)
        return user_text
    else:                   #失败返回
        return False



# 文字转语音
def text_to_speech(ai_text):
    
    # spd：语速0-9，vol：音量0-15，per：发音人选择 0女 1男 3男 4女
    result = client.synthesis(ai_text, 'zh', 1, {
        'vol': 5, 'per': 4, 'spd': 3
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        print('识别成功')
        with open('./audiofile/aisay.mp3', 'wb') as f:
            f.write(result)
        os.system('mpg123 '+'./audiofile/aisay.mp3')



if __name__=='__main__':    # 模块测试

    speech_to_text()
    text_to_speech("四是四，十是十")
    
