import sys
import os
import time
import logging
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
''''''

from waveshare_epd import epd2in13_V2
from weather import weather
from screen import screen2in13

'''temperature = ""
skycon = ""
stat = 1'''


anyway = False#for test


epd = epd2in13_V2.EPD()  # 实例化墨水屏对象
# logging 只需要设置一次，之后调用只需要import logging即可
#logging.basicConfig(filename="clock.log", level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG
                    , format='%(asctime)s;;%(name)s;;%(levelname)s;;%(message)s'
                    , datefmt='%Y-%m-%d %H:%M:%S'
                    , filename='/var/log/clock.log')

try:
    logging.info("show time")
    #初始化屏幕并清屏
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)#初始化和退出睡眠后调用，full_update全刷性
    #epd.Clear(0xFF)

    # 设置背景图片
    logging.info("init screen")
    screen = screen2in13.Screen()
    logging.info("draw backimage")
    screen.drawbackimg()
    logging.info("set background img")
    epd.displayPartBaseImage(epd.getbuffer(screen.getimage()))

    #设置为局部刷新后设置局部刷新的图片
    logging.info("init for part update")
    epd.init(epd.PART_UPDATE)
    logging.info("draw date")
    screen.drawdateimg()
    epd.displayPartial(epd.getbuffer(screen.getimage()))

    #第一次启动设置天气
    logging.info("first start to set weather")
    weather_thread = weather.Thread_weather()
    weather_thread.start()
    logging.info("sleep 3s")
    time.sleep(3)#休眠3s，等待获取天气信息
    result = weather_thread.get_result()  # 获取天气数
    screen.drawweatherimg(result)

    while (True):
        while (True):
            if time.localtime()[5] == 0 or anyway:#当秒数归零的时候更新时间
                #画一个矩形，填充为白色，覆盖之前画上的图片
                logging.info("update time")
                screen.drawtimeimg()
                if time.localtime()[3] == 0 or anyway:#小时归零后更新日期
                    #更新日期
                    logging.info("update date")
                    screen.drawdateimg()
                if time.localtime()[4] == 0 or anyway:#分钟归零后更新天气, 每小时更新一次
                    logging.info("get weather data")
                    result = weather_thread.get_result()#获取天气数据
                    screen.drawweatherimg(result)
                epd.displayPartial(epd.getbuffer(screen.getimage()))
                logging.info("jump second loop")
                break
            logging.info("sleep 1s")
            time.sleep(1)#休眠1s
        logging.info("sleep 55s")
        time.sleep(55)#休眠50s
        if time.localtime()[4] == 59 or anyway:#每小时更新一下天气
            logging.info("start a thread to get weather")
            weather_thread = weather.Thread_weather()
            weather_thread.start()
            #time.sleep(1)#for test

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    epd2in13_V2.epdconfig.module_exit()
    exit()
    ''''''
