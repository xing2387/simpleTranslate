# -*- coding:utf-8 -*-

import hashlib
import time
import requests
import json

appid = None
secret = None

urlFormat = 'https://fanyi-api.baidu.com/api/trans/vip/translate?q={}&from=auto&to=auto&appid={}&salt={}&sign={}'.format


def getSign(appid, query, salt, secret):
    text = str(appid) + str(query) + str(salt) + str(secret)
    print(text)
    return hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()


def getTranslate(query):
    initAppid()
    salt = int(time.time())
    sign = getSign(appid, query, salt, secret)
    url = urlFormat(query, appid, salt, sign)
    print(url)
    jsonText = json.loads(requests.get(url).text)
    print(str(jsonText))
    translateText = ""
    for result in jsonText["trans_result"]:
        translateText += (result["dst"] + "\n")
    return translateText


def initAppid():
    global appid
    global secret
    if not appid:
        with open("config", "r") as f:
            lines = f.readlines()
            appid = lines[0][0:-1]
            secret = lines[1]

# getTranslate("hello")
