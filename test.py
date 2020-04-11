
'''from weather import weather
stat, temperature, skycon = weather.Weather().getweather()
print(stat)
print(type(str(temperature)))
print(skycon)'''

import requests
try:
    r = requests.get('https://api.caiyunapp.com/v2.5/TAkhjf8d1nlSlspN/121.6544,25.1552/daily.json')
    print(r)
    print(r.content)
    res = r.json()
    print(res)
    print("********************************")
    print(res['result']['daily']['temperature'][1]['max'])
    print(res['result']['daily']['skycon'][1])
except requests.exceptions.ConnectionError as why:
    print(why)


dirt = {'a':1}
if 'alert' in dirt.keys():#判断字典中是否有某个key
    print("y")
else:
    print("n")

'''

r = requests.get('https://api.caiyunapp.com/v2.5/TAkhjf8d1nlSlspN/121.6544,25.1552/realtime.json')
print(r.content)
res = r.json()
print(res)
print("********************************")
print(res["result"]["realtime"]["temperature"])

'''
'''
import time
t = time.localtime()
print(t)
print(t[5])
print(time.localtime()[5] == 0)

while True:
    while True:
        if time.localtime()[5] == 0:
            print(time.localtime())
            break
        print("sleep 1s")
        time.sleep(1)
    print("sleep 50s")
    time.sleep(50)#休眠1s
'''


'''#图片像素转换
import os
for i in range(1, 13):
    url = os.path.join("/home/qian/%s.jpg"%(str(i)))
    name = os.path.join("1%s.jpg"%str(i))
    img = Image.open(url)
    img = img.resize((50, 50))
    img.save(name)
#图片二值化并取反色
img.show()
img = img.convert("L")
img.show()
from PIL import ImageOps
img = ImageOps.invert(img)
img.show()
img.save("weather.jpg")
img = img.convert("1")
img.show()
img.save("weather2.jpeg", "jpeg")'''
