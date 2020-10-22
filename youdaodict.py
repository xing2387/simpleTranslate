import requests
import json


# keyfrom和key来源：
# 1.  https://www.cnblogs.com/zhuweiblog/p/5200777.html :
# http://fanyi.youdao.com/openapi.do?keyfrom=youdaoci&key=694691143&type=data&doctype=xml&version=1.1&q=hello
# 2.  https://blog.csdn.net/x_iya/article/details/45095693 :
# http://fanyi.youdao.com/openapi.do?keyfrom=neverland&key=969918857&type=data&doctype=json&version=1.1&q=good
# http://apii.dict.cn/mini.php?q=dog

urlFormat = "http://fanyi.youdao.com/openapi.do?keyfrom=neverland&key=969918857&type=data&doctype=json&version=1.1&q={}".format


def getTranslate(query):
    jsonObj = json.loads(requests.get(urlFormat(query)).text)
    print(jsonObj)
    result = "翻译:\n"
    if "translation" in jsonObj:
        for x in jsonObj["translation"]:
            result += ("    " + str(x) + "\n")
    if ("basic" in jsonObj) and ("explains" in jsonObj["basic"]):
        result = ("英汉翻译:" + "\n")
        result += listToStr(jsonObj["basic"]["explains"], "    ", "\n")
    if "web" in jsonObj:
        result += "网络释义:\n"
        for itemDict in jsonObj["web"]:
            value = listToStr(itemDict["value"], "", "；")
            result += ("    " + str(itemDict["key"]) + ": " + value + "\n")
    return result


def listToStr(sourceList, separatorBefore, separatorAfter):
    result = ""
    if sourceList != None:
        for x in sourceList:
            result += str(separatorBefore) + str(x) + str(separatorAfter)
    return result


# print(getTranslate("good good"))
'''
{
    "translation": [
        "“好了好了”"
    ],
    "query": "\"good good\"",
    "errorCode": 0
}

英汉翻译:
    n. 好处；善行；慷慨的行为
    adj. 好的；优良的；愉快的；虔诚的
    adv. 好
    n. (Good)人名；(英)古德；(瑞典)戈德
网络释义:
    good: 好的
    Good morning: 早上好
    for good: 永久地

{
    "translation": [
        "好"
    ],
    "basic": {
        "us-phonetic": "ɡʊd",
        "phonetic": "ɡʊd",
        "uk-phonetic": "ɡʊd",
        "explains": [
            "n. 好处；善行；慷慨的行为",
            "adj. 好的；优良的；愉快的；虔诚的",
            "adv. 好",
            "n. (Good)人名；(英)古德；(瑞典)戈德"
        ]
    },
    "query": "good",
    "errorCode": 0,
    "web": [
        {
            "value": [
                "好的",
                "善",
                "良好"
            ],
            "key": "good"
        },
        {
            "value": [
                "早上好",
                "早安",
                "早晨好"
            ],
            "key": "Good morning"
        },
        {
            "value": [
                "永久地",
                "永远",
                "永恒地"
            ],
            "key": "for good"
        }
    ]
}
'''
