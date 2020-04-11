'''import sys
import os
import time
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
wdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'weather')

if os.path.exists(libdir):
    sys.path.extend([libdir, wdir])'''

import logging

'''mport weather
{'status': 'ok', 'api_version': 'v2.5', 'api_status': 'active', 'lang': 'zh_CN', 'unit': 'metric', 'tzshift': 28800, 'timezone': 'Asia/Shanghai', 'server_time': 1585313626, 'location': [31.3844, 117.2697], 'result': {'realtime': {'status': 'ok', 'temperature': 8.21, 'humidity': 0.9, 'cloudrate': 1.0, 'skycon': 'LIGHT_RAIN', 'visibility': 7.3, 'dswrf': 28.6, 'wind': {'speed': 14.4, 'direction': 17.0}, 'pressure': 102100.78, 'apparent_temperature': 5.2, 'precipitation': {'local': {'status': 'ok', 'datasource': 'radar', 'intensity': 0.0925}, 'nearest': {'status': 'ok', 'distance': 0.43, 'intensity': 0.1875}}, 'air_quality': {'pm25': 15.0, 'pm10': 46.0, 'o3': 71.0, 'so2': 6.0, 'no2': 22.0, 'co': 0.4, 'aqi': {'chn': 46.0, 'usa': 57.0}, 'description': {'chn': '优', 'usa': '良'}}, 'life_index': {'ultraviolet': {'index': 0.0, 'desc': '无'}, 'comfort': {'index': 8, 'desc': '很冷'}}}, 'primary': 0, 'alert': {'status': 'ok', 'content': [{'province': '安徽省', 'status': '预警中', 'code': '0501', 'description': '庐江县24小时内可能受大风影响,平均风力可达6级以上，或者阵风7级以上；或者已经受大风影响, 平均风力为6～7级，或者阵风7～8级并可能持续。请注意防范！', 'pubtimestamp': 1585235100.0, 'city': '合肥市', 'adcode': '340124', 'regionId': '101220106', 'latlon': [31.25555, 117.2878], 'county': '庐江县', 'alertId': '34012441600000_20200326230506', 'request_status': 'ok', 'source': '国家预警信息发布中心', 'title': '庐江县气象台发布大风蓝色预警[IV级/一般]', 'location': '安徽省合肥市庐江县'}, {'province': '安徽省', 'status': '预警中', 'code': '0401', 'description': '48小时内全市最低气温将下降8～11℃，平均风力4～5级，阵风8级左右，请注意防范！', 'pubtimestamp': 1585189560.0, 'city': '合肥市', 'adcode': '340100', 'regionId': 'unknown', 'latlon': [31.820586, 117.227239], 'county': '无', 'alertId': '34010041600000_20200326102954', 'request_status': 'ok', 'source': '国家预警信息发布中心', 'title': '合肥市气象局发布寒潮蓝色预警[IV级/一般]', 'location': '安徽省合肥市'}]}}}
from PIL import Image,ImageDraw,ImageFont
import os
from .tt import *
picdir = setting.get_picdir()
wdir = setting.get_wdir()stat, sy, o = w.get_weather()
print(stat)
print(sy)
print(o)'''

'''th = weather.Thread_weather()
th.start()
#time.sleep(1)
th.join()#等待进程结束后在执行后续的内容
sta, tem, sky = th.get_result()
print(sta)
print(tem)
print(sky)img = Image.open('晴.jpeg')
img = img.resize((50, 50))
img.show()'''
''''skycon = "晴"
print(picdir)
weatherpicdir = os.path.join(picdir, os.path.join("/%s.jpg"%skycon))
weatherpicdir1 = os.path.join("%s/%s.jpg"%(picdir, skycon))
print(weatherpicdir)
print(weatherpicdir1)
ALERTLIS = ["", "台风", "暴雨", "暴雪", "寒潮", "大风", "沙尘暴", "高温", "干旱", "雷电", "冰雹", "霜冻", "大雾", "霾"
    , "道路结冰", "森林火灾", "雷电大风"]

LEVEL = ["", "蓝色", "黄色", "橙色", "红色"]

alert = {"code":"0901"}

alertnum = int(alert["code"])
print(alertnum)
alert = ALERTLIS[alertnum//100] + LEVEL[alertnum%10] + "预警"
print(alert)'''
'''
经过函数处理后image对象未发生改变
from PIL import Image,ImageDraw,ImageFont

time_image = Image.new('1', (122, 250), 255)
time_draw = ImageDraw.Draw(time_image)
print("-------time_image-------")
print(time_image)
print("-------time_draw-------")
print(time_draw)
def drawimg(img):
    img.rectangle((1, 1, 20, 20), fill=0)


time_draw2 = drawimg(time_draw)
print("-------time_image-------")
print(time_image)
print("-------time_draw2-------")
print(time_draw2)
print("-------time_draw-------")
print(time_draw)
print(type(time_draw))

'''

#logging.basicConfig(level=logging.DEBUG, format='%(name)s%(levelname)s%(asctime)s%(message)s', filename='test.log')
logging.basicConfig(level=logging.DEBUG
                    , format='%(asctime)s:%(name)s:%(levelname)s:%(message)s'
                    , datefmt='%Y-%m-%d %H:%M:%S')
'''
console = logging.StreamHandler()# 定义console handle
console.setLevel(logging.INFO)# 设置日志级别
format = logging.Formatter('%(name)s%(levelname)s%(asctime)s%(message)s')#定义该handle格式
console.setFormatter(format)#设置该handle格式
logging.getLogger().addHandler(console)
'''
logging.info("aaaaa")
logging.info("bbbb")
logging.info("cccc")

'''直接写from .settings import Settings会报No module named '__main__.settings'的错误
    直接import settings也会报无法引用的错误，
    解决办法：from 文件夹名 import 文件名
'''