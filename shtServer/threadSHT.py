
# -*- coding: utf-8 -*-

import threading
from sys import exit

from loggerSHT import logger

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
                logger.log_info("Exeception happends: " + str(err) + ", rerunning...")
                continue
            except KeyboardInterrupt:
                logger.log_info("exit from KeyboardInterrupt")
                exit(1)
