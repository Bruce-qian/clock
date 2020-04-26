import os
import sys
from PIL import Image,ImageDraw,ImageFont
import logging
import time
libdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd2in13_V2


height = 250
width = 122
defaultpic = "13"

class Screen(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "screen"):
            cls.screen = super(Screen, cls).__new__(cls)
        return cls.screen
    def __init__(self):
        self.__image = Image.new('1', (height, width), 255)
        self.__draw = ImageDraw.Draw(self.__image)
        self.__picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'pic')
        self.__font12 = ImageFont.truetype(os.path.join(self.__picdir, 'Font.ttc'), 12)
        self.__font15 = ImageFont.truetype(os.path.join(self.__picdir, 'Font.ttc'), 15)
        self.__font24 = ImageFont.truetype(os.path.join(self.__picdir, 'Font.ttc'), 24)
        self.__font30 = ImageFont.truetype(os.path.join(self.__picdir, 'Font.ttc'), 30)
        self.__font35 = ImageFont.truetype(os.path.join(self.__picdir, 'Font.ttc'), 35)
        self.__font40 = ImageFont.truetype(os.path.join(self.__picdir, 'Font.ttc'), 40)
        logging.info("init screen")
        self.__epd = epd2in13_V2.EPD()  # 实例化墨水屏对象
        logging.info("set full update")
        self.__epd.init(self.__epd.FULL_UPDATE)  # 设置为全局刷新
        self.drawbackimg()
        self.__epd.displayPartBaseImage(self.__epd.getbuffer(self.__image))  # 绘制背景图片


    def drawbackimg(self):
        '''
        画屏幕的背景图片
        :return:
        '''
        logging.info("draw backimg")
        self.__draw.line((0, 45, height, 45), fill=0)#画横线
        self.__draw.line((80, 45, 80, 120), fill=0)#第一条竖线
        self.__draw.line((162, 45, 162, 120), fill=0)#第二条竖线
        self.__draw.text((170, 80), u"数据来自", font=self.__font15, fill=0)
        self.__draw.text((170, 100), u"彩云科技", font=self.__font15, fill=0)
        #self.__time_draw.text((10, 10), u"同步中", font=font15, fill=0)
        self.__draw.text((125, 16), time.strftime('%Y-%m-%d'), font=self.__font24, fill=0)

    def drawweatherimg(self, result):
        '''
        绘制天气数据， 网络状态与天气一起更新
        :return:
        '''
        logging.info("draw weatherimg")
        stat = result['stat']
        temperature = result['realtimetem']
        skycon = result['realtimeskycon']
        maxftem = result['maxfcasttem']
        minftem = result['minfcasttem']
        fskycon = result['fcastskycon']
        alert = result['alert']
        # 判断网络是否正常
        if stat:
            logging.info("network faill")
            netstat = "连接异常"
            self.__draw.rectangle((125, 1, 250, 15), fill=255)
            self.__draw.text((180, 1), netstat, font=self.__font15, fill=0)
        else:
            logging.info("network pass")
            netstat = "连接正常"
            self.__draw.rectangle((125, 1, 250, 15), fill=255)
            self.__draw.text((180, 1), netstat, font=self.__font15, fill=0)
            # 实时天气
            logging.info("update realtime weather")
            self.__draw.rectangle((1, 50, 79, 120), fill=255)
            if skycon == "":
                weatherpicdir = os.path.join("%s/%s.jpg" % (self.__picdir, defaultpic))
            else:
                weatherpicdir = os.path.join("%s/%s.jpg" % (self.__picdir, skycon))  # 天气图片路径
            weatherpic = Image.open(weatherpicdir)
            self.__image.paste(weatherpic, (15, 50))
            self.__draw.text((5, 100), temperature, font=self.__font15, fill=0)
            self.__draw.text((35, 100), skycon, font=self.__font15, fill=0)
            # 预报天气
            logging.info("update forecaste weather")
            self.__draw.rectangle((81, 50, 160, 120), fill=255)
            if fskycon == "":
                fweatherpicdir = os.path.join("%s/%s.jpg" % (self.__picdir, defaultpic))
            else:
                fweatherpicdir = os.path.join("%s/%s.jpg" % (self.__picdir, fskycon))  # 天气图片路径
            fweatherpic = Image.open(fweatherpicdir)
            self.__image.paste(fweatherpic, (95, 50))
            temrange = os.path.join("%s-%s" % (minftem, maxftem))
            self.__draw.text((85, 100), temrange, font=self.__font15, fill=0)
            self.__draw.text((125, 100), fskycon, font=self.__font15, fill=0)
            # 预警信息
            logging.info("update alert")
            self.__draw.rectangle((170, 50, 250, 75), fill=255)
            self.__draw.text((170, 50), alert, font=self.__font15, fill=0)

    def drawtimeimg(self):
        '''
        绘制时间数据
        :return:
        '''
        logging.info("draw timeimg")
        self.__draw.rectangle((1, 1, 100, 43), fill=255)
        self.__draw.text((1, 1), time.strftime('%H:%M'), font=self.__font40, fill=0)

    def drawdateimg(self):
        '''
        绘制日期数据
        :return:
        '''
        logging.info("draw dateimg")
        self.__draw.rectangle((125, 16, 250, 43), fill=255)
        self.__draw.text((125, 16), time.strftime('%Y-%m-%d'), font=self.__font24, fill=0)

    def getimage(self):
        logging.info("get image")
        return self.__image

    def display(self):
        logging.info("set part update and display")
        self.__epd.init(self.__epd.PART_UPDATE)  # 设置局部刷新
        self.__epd.displayPartial(self.__epd.getbuffer(self.__image))

    def clean(self):
        logging.info("set full update and clean")
        self.__epd.init(self.__epd.FULL_UPDATE)
        self.__epd.Clear(0xFF)

    def exit(self):
        logging.info("exit device")
        epd2in13_V2.epdconfig.module_exit()


if __name__ == "__main__":
    screen = Screen()
    screen.drawdateimg()
    screen.display()
    screen.drawtimeimg()
    screen.display()