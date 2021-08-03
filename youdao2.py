# -*- coding:utf-8 -*-

import requests
from urllib.parse import urlencode
import json


# urlFormat = 'http://dict.youdao.com/jsonapi?jsonversion=2&client=mobile&q={}&dicts={"count":99,"dicts":[["ec","ce","newcj","newjc","kc","ck","fc","cf","multle","jtj","pic_dict","tc","ct","typos","special","tcb","baike","lang","simple","wordform","exam_dict","ctc","web_search","auth_sents_part","ec21","phrs","input","wikipedia_digest","ee","collins","ugc","media_sents_part","syno","rel_word","longman","ce_new","le","newcj_sents","blng_sents_part","hh"],["ugc"],["longman"],["newjc"],["newcj"],["web_trans"],["fanyi"]]}&keyfrom=mdict.7.2.0.android&model=honor&mid=5.6.1&imei=659135764921685&vendor=wandoujia&screen=1080x1800&ssid=superman&network=wifi&abtest=2&xmlVersion=5.1'.format

def urlFormat(q):
     return 'http://dict.youdao.com/jsonapi?jsonversion=2&client=mobile&'+urlencode({"q":q})+'&dicts=%7B%22count%22%3A99%2C%22dicts%22%3A%5B%5B%22ec%22%2C%22ce%22%5D%2C%5B%22web_trans%22%5D%2C%5B%22fanyi%22%5D%5D%7D&keyfrom=mdict.7.2.0.android&model=honor&mid=5.6.1&imei=659135764921685&vendor=wandoujia&screen=1080x1800&ssid=superman&network=wifi&abtest=2&xmlVersion=5.1'

def getTranslate(query):
     jsonObj = None
     print(urlFormat(query))
     try:
          jsonObj = json.loads(requests.get(urlFormat(query)).text)
     except Exception as e:
          print(e)
     if jsonObj == None:
          print("query for '{}' failed".format(query))
          return
     # print(jsonObj)
     result = ""
     if "fanyi" in jsonObj:
          result = jsonObj["fanyi"]["tran"]
     elif "ec" in jsonObj:
          word = jsonObj["ec"]["word"]
          for w in word:
               result += w["usphone"]+"\n" if "usphone" in w else ""
               for tr in w["trs"]:
                    result += getEcStr(tr)+"\n"
     elif "ce" in jsonObj:
          word = jsonObj["ce"]["word"]
          for w in word:
               result += w["usphone"]+"\n" if "usphone" in w else ""
               for tr in w["trs"]:
                    result += getCeStr(tr)
     return result


def getEcStr(dd):
     if type(dd) is dict:
          return getEcStr(list(dd.values())[0])
     elif type(dd) is list:
          return getEcStr(dd[0])
     else:
          return str(dd)


def getCeStr(dd):
     result=""
     if type(dd) is list:
          for ll in dd:
               result += getCeStr(ll)
     elif type(dd) is dict:
          if "#text" in dd:
               return dd["#text"]+"\n"
          for kk in list(dd.keys()):
               result += getCeStr(dd[kk])
     return result




def listToStr(sourceList, separatorBefore, separatorAfter):
     result = ""
     if sourceList != None:
          for x in sourceList:
               result += str(separatorBefore) + str(x) + str(separatorAfter)
     return result


# print(getTranslate("monitoring"))