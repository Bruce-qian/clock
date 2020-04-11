import os
import sys

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
print(libdir)
if os.path.exists(libdir):
    sys.path.append(libdir)
from waveshare_epd import epd2in13_V2

os.system("kill -2 $(ps aux | grep 'clockback' | grep -v 'grep' | awk '{print $2}')")
epd = epd2in13_V2.EPD()  # 实例化墨水屏对象
#print(re)
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)
epd2in13_V2.epdconfig.module_exit()