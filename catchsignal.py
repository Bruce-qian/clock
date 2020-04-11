#!/usr/bin/python3
import signal
import time
import sys
import logging

logging.basicConfig(filename='catch.log', level=logging.DEBUG)







def run():
    while True:
        logging.info("sleep 1s")
        time.sleep(1)

def handle(signalnum, frame):
    logging.info('stop run')
    print(signalnum)
    sys.exit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle)
    run()