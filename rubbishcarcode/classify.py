import jieba
import pandas as pd

rubbish = dict()#创建一个字典
rubbish_data = pd.read_csv('./csvfile/rubbish.csv', encoding='gbk')#rubbish_data为dataframe数据
r = list(rubbish_data["可回收物"])#将series数组转化为列表
r = dict.fromkeys(r, '可回收物')#添加键值变为字典
rubbish.update(r)


r = list(rubbish_data["有害垃圾"])
r = dict.fromkeys(r, '有害垃圾')
rubbish.update(r)

r = list(rubbish_data["厨余垃圾"])
r = dict.fromkeys(r, '厨余垃圾')
rubbish.update(r)

r = list(rubbish_data["其他垃圾"])
r = dict.fromkeys(r, '其他垃圾')
rubbish.update(r)

#调节单个词语词频，使其被正确分割
jieba.suggest_freq('有害垃圾', True)
jieba.suggest_freq('厨余垃圾', True)
jieba.suggest_freq('可回收物', True)
jieba.suggest_freq('其他垃圾', True)


def get_type(string):
    
    seg_list = jieba.lcut(string, cut_all=True)  # 全模式，词义模糊但匹配成功率高
    #jieba.cut返回一个可迭代的generator而jieba.lcut返回的则是列表，方便遍历
    print("/".join(seg_list))
    #list1 = ['有害垃圾','厨余垃圾','可回收物','其他垃圾']
    #print(rubbish)
    for x in seg_list:
        if x in rubbish.keys():
            print(x)
            return x,rubbish[x]
        elif x in rubbish.values():
            print(x)
            return None,x

if __name__=='__main__':    # 模块测试

    string = "废纸是什么垃圾"

    result = get_type(string)
    if result==False:   # 没有说任何垃圾
        print('眼不见心不烦，不如当没看见吧')
    elif result[0]!=None:
        print(result[0]+'是'+result[1])
    else:
        print( result[1]+"箱已打开")
