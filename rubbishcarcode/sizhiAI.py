import json
import urllib.request

# 思知机器人 API
ROBOT_KEY = "b32658188b167e341dcef9ce5597028b"
API_URL = "https://api.ownthink.com/bot"


# 思知机器人处理
def ai_think(user_text):
    req = {
        "spoken": user_text,
        "appid": ROBOT_KEY,
        "userid": "JqelL1gY"
    }
    # json.dumps()和json.loads()是json格式处理函数（可以将json理解为是字符串）
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')
    # json.dumps()函数是将一个Python数据类型列表进行json格式的编码（可以这么理解，json.dumps()函数是将字典转化为字符串）

    # 在request对象中添加相应头信息
    http_post = urllib.request.Request(url=API_URL, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    # 函数是将json格式数据转换为字典（可以这么理解，json.loads()函数是将字符串转化为字典）
    response_dic = json.loads(response_str)
    ai_text = response_dic['data']['info']['text']
    print("AI说: " + ai_text)
    return ai_text

if __name__=='__main__':    # 模块测试
    ai_think('西安今天天气')
