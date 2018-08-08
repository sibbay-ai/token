
import threading
from sys import exit
from time import sleep
from .logger import logger


class ThreadSHT(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        while True:
            try:
                self.func(*self.args)
                continue
            except Exception as err:
                logger.info("Exeception happends: " + str(err) + " at " + self.name + ",  rerunning...")
                sleep(1)
                continue
            except KeyboardInterrupt:
                logger.info("exit from KeyboardInterrupt")
                exit(1)
