import requests
import threading
import time
import logging
import json
import re
import os

SKYCONDIC = {"CLEAR_DAY":"晴", "CLEAR_NIGHT":"晴", "PARTLY_CLOUDY_DAY":"多云", "PARTLY_CLOUDY_NIGHT":"多云"
    , "CLOUDY":"阴", "LIGHT_HAZE":"轻度雾霾", "MODERATE_HAZE":"中度雾霾", "HEAVY_HAZE":"重度雾霾", "LIGHT_RAIN":"小雨"
    , "MODERATE_RAIN":"中雨", "HEAVY_RAIN":"大雨", "STORM_RAIN":"暴雨", "FOG":"雾", "LIGHT_SNOW":"小雪", "MODERATE_SNOW":"中雪"
    , "HEAVY_SNOW":"大雪", "STORM_SNOW":"暴雪", "DUST":"浮尘", "SAND":"沙尘", "WIND":"大风"}

ALERTLIS = ["", "台风", "暴雨", "暴雪", "寒潮", "大风", "沙尘暴", "高温", "干旱", "雷电", "冰雹", "霜冻", "大雾", "霾"
    , "道路结冰", "森林火灾", "雷电大风"]

LEVEL = ["", "蓝色", "黄色", "橙色", "红色"]

configfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
#print(configfile)
with open(configfile, encoding="utf-8") as f:
    config = json.load(f)
location = "%s,%s" % (config["location"]["longitude"], config["location"]["latitude"])
token = config["token"]
realtimeurl = re.sub("token", token, re.sub("location", location, config["url"]["realtimeurl"]))
forecasturl = re.sub("token", token, re.sub("location", location, config["url"]["fcasturl"]))

class Weather:
    def __init__(self, rtimeurl, fcasturl):
        self.__realtimeurl = rtimeurl#获取实时天气url
        self.__forecasturl = fcasturl#获取未来几天天气的url

    def get_weather(self):
        try:
            realtimeresponse = requests.get(self.__realtimeurl)
            forecastresponse = requests.get((self.__forecasturl))
            logging.info("request success")
        except:
            logging.info("request fail")
            return {'stat':1, 'realtimetem':'', 'realtimeskycon':'', 'maxfcasttem':'', 'minfcasttem':'', 'fcastskycon':'', 'alert':''}
        realtimejson = realtimeresponse.json()
        forecastjson = forecastresponse.json()
        #print(realtimejson)
        realtimetemperature = str(int(realtimejson['result']['realtime']['temperature']))
        #print(type(temperature))
        if "alert" in realtimejson['result']:
            alertnum = ""
            #alertnum = realtimejson['result']['alert']['content'][0]['code']#获取预警信息
            #print(realtimejson['result']['alert']['content'].items)
        else:
            alertnum = ""
        #alertnum = "0901"# for test
        if alertnum == "":
            alert = "无预警"
        else:
            alert = ALERTLIS[int(alertnum)//100] + LEVEL[int(alertnum)%10]
        #print(alert)
        realtimeskycon = SKYCONDIC[realtimejson['result']['realtime']['skycon']]
        maxfcasttem = str(int(forecastjson['result']['daily']['temperature'][1]['max']))
        minfcasttem = str(int(forecastjson['result']['daily']['temperature'][1]['min']))
        fcastskycon = SKYCONDIC[forecastjson['result']['daily']['skycon'][1]['value']]
        return {'stat':0, 'realtimetem': realtimetemperature, 'realtimeskycon':realtimeskycon, 'maxfcasttem':maxfcasttem, 'minfcasttem':minfcasttem, 'fcastskycon':fcastskycon, 'alert':alert}


class Thread_weather(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        '''self.__stat = 1
        self.__realtimetemperature = ""
        self.__realtimeskycon = ""
        self.__maxfcasttem = ""
        self.__minfcasttem = ""
        self.__fcastskycon = ""'''
        self.__result = dict()

    def run(self) -> None:
        w = Weather(realtimeurl, forecasturl)
        self.__result = w.get_weather()
    def get_result(self):
        return self.__result

if __name__ == '__main__':
    weather_thread = Thread_weather()
    weather_thread.start()
    time.sleep(3)
    #sta, rtem, rsky , maxftem, minftem, fsky= weather_thread.get_result()
    resu = weather_thread.get_result()
    for k, v in resu.items():
        print("%s:%s"%(k, v))
        ''' print(sta)
    print(rtem)
    print(rsky)
    print(maxftem)
    print(minftem)
    print(fsky)'''
