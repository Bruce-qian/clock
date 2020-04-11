import sys
import os
import time
from PIL import Image,ImageDraw,ImageFont
import logging

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
''''''

from waveshare_epd import epd2in13_V2
from weather import weather

'''temperature = ""
skycon = ""
stat = 1'''
defaultpic = "13"
result = dict()

anyway = False#for test
font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
logging.basicConfig(level=logging.DEBUG
                    , format='%(asctime)s:%(name)s:%(levelname)s:%(message)s'
                    , datefmt='%Y-%m-%d %H:%M:%S')
#logging.basicConfig(filename="clock.log", level=logging.DEBUG)

try:
    logging.info("show time")
    #初始化屏幕并清屏
    epd = epd2in13_V2.EPD()#实例化墨水屏对象
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)#初始化和退出睡眠后调用，full_update全刷性
    #epd.Clear(0xFF)

    # 设置背景图片
    logging.info("show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    time_draw.line((0, 45, epd.height, 45), fill=0)
    time_draw.line((80, 45, 80, 120), fill=0)
    time_draw.line((162, 45, 162, 120), fill=0)
    time_draw.text((170, 80), u"数据来自", font=font15, fill=0)
    time_draw.text((170, 100), u"彩云科技", font=font15, fill=0)
    logging.info("set background img")
    epd.displayPartBaseImage(epd.getbuffer(time_image))

    #设置为局部刷新后设置局部刷新的图片
    logging.info("init for part update")
    epd.init(epd.PART_UPDATE)
    time_draw.text((10, 10), u"同步中", font=font15, fill=0)
    time_draw.text((125, 16), time.strftime('%Y-%m-%d'), font=font24, fill=0)
    epd.displayPartial(epd.getbuffer(time_image))

    #第一次启动设置天气
    logging.info("first start to set weather")
    weather_thread = weather.Thread_weather()
    weather_thread.start()
    logging.info("sleep 3s")
    time.sleep(3)#休眠3s，等待获取天气信息
    result = weather_thread.get_result()  # 获取天气数
    stat = result['stat']
    temperature = result['realtimetem']
    skycon = result['realtimeskycon']
    maxftem = result['maxfcasttem']
    minftem = result['minfcasttem']
    fskycon = result['fcastskycon']
    alert = result['alert']
    #判断网络是否正常
    if stat:
        logging.info("network fail")
        netstat = "连接异常"
    else:
        logging.info("network pass")
        netstat = "连接正常"
    time_draw.rectangle((125, 1, 250, 15), fill=255)
    time_draw.text((180,1), netstat, font=font15, fill=0)
    #实时天气
    time_draw.rectangle((1, 50, 79, 120), fill=255)
    if skycon == "":
        weatherpicdir = os.path.join("%s/%s.jpg"%(picdir, defaultpic))
    else:
        weatherpicdir = os.path.join("%s/%s.jpg"%(picdir, skycon))#天气图片路径
    weatherpic = Image.open(weatherpicdir)
    time_image.paste(weatherpic, (15, 50))
    time_draw.text((5, 100), temperature, font=font15, fill=0)
    time_draw.text((35, 100), skycon, font=font15, fill=0)
    #预报天气
    time_draw.rectangle((81, 50, 160, 120), fill=255)
    if fskycon == "":
        fweatherpicdir = os.path.join("%s/%s.jpg" % (picdir, defaultpic))
    else:
        fweatherpicdir = os.path.join("%s/%s.jpg" % (picdir, fskycon))  # 天气图片路径
    fweatherpic = Image.open(fweatherpicdir)
    time_image.paste(fweatherpic, (95, 50))
    temrange = os.path.join("%s-%s"%(minftem, maxftem))
    time_draw.text((85, 100), temrange, font=font15, fill=0)
    time_draw.text((125, 100), fskycon, font=font15, fill=0)
    #预警信息
    time_draw.rectangle((170, 50, 250, 75), fill=255)
    time_draw.text((170, 50), alert, font=font15, fill=0)
    while (True):
        while (True):
            if time.localtime()[5] == 0 or anyway:#当秒数归零的时候更新时间
                #画一个矩形，填充为白色，覆盖之前画上的图片
                logging.info("update time")
                time_draw.rectangle((1, 1, 100, 43), fill=255)
                time_draw.text((1, 1), time.strftime('%H:%M'), font=font40, fill=0)
                if time.localtime()[3] == 0 or anyway:#小时归零后更新日期
                    #更新日期
                    logging.info("update date")
                    time_draw.rectangle((125, 16, 250, 43), fill=255)
                    time_draw.text((125, 16), time.strftime('%Y-%m-%d'), font=font24, fill=0)
                if time.localtime()[4] == 0 or anyway:#分钟归零后更新天气, 每小时更新一次
                    logging.info("get weather data")
                    result = weather_thread.get_result()#获取天气数据
                    stat = result['stat']
                    temperature = result['realtimetem']
                    skycon = result['realtimeskycon']
                    maxftem = result['maxfcasttem']
                    minftem = result['minfcasttem']
                    fskycon = result['fcastskycon']
                    alert = result['alert']
                    # 判断网络是否正常
                    if stat:
                        logging.info("network fail")
                        netstat = "连接异常"
                    else:
                        logging.info("network pass")
                        netstat = "连接正常"
                    time_draw.rectangle((125, 1, 250, 15), fill=255)
                    time_draw.text((180, 1), netstat, font=font15, fill=0)
                    logging.info("update weather")
                    if not stat or anyway:#获取成功更新天气信息，不成功打印提示信息
                        #实时天气
                        time_draw.rectangle((1, 50, 79, 120), fill=255)
                        weatherpicdir = os.path.join("%s/%s.jpg" % (picdir, skycon))  # 打开对应的天气图片
                        weatherpic = Image.open(weatherpicdir)
                        time_image.paste(weatherpic, (15, 50))
                        time_draw.text((5, 100), temperature, font=font15, fill=0)
                        time_draw.text((35, 100), skycon, font=font15, fill=0)
                        #预报天气
                        time_draw.rectangle((81, 50, 160, 120), fill=255)
                        if fskycon == "":
                            fweatherpicdir = os.path.join("%s/%s.jpg" % (picdir, defaultpic))
                        else:
                            fweatherpicdir = os.path.join("%s/%s.jpg" % (picdir, fskycon))  # 天气图片路径
                        fweatherpic = Image.open(fweatherpicdir)
                        time_image.paste(fweatherpic, (95, 50))
                        temrange = os.path.join("%s-%s"%(minftem, maxftem))
                        time_draw.text((85, 100), temrange, font=font15, fill=0)
                        time_draw.text((125, 100), fskycon, font=font15, fill=0)
                        # 预警信息
                        time_draw.rectangle((170, 50, 250, 75), fill=255)
                        time_draw.text((170, 50), alert, font=font15, fill=0)
                    else:
                        time_draw.rectangle((1, 50, 80, 120), fill=255)
                        time_draw.text((1,50), "error", font=font24, fill=0)
                epd.displayPartial(epd.getbuffer(time_image))
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
