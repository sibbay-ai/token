
# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler

import infoSHT

# log level
LOGGER_LEVEL = logging.INFO

# class loggerSHT
class LoggerSHT:
    def __init__(self, file_name, logger_name):
        # log handler, one log file each day
        logHandler = TimedRotatingFileHandler(file_name, when="midnight")
        # log fromat
        logFormatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        logHandler.setFormatter(logFormatter)
        # log name
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(logHandler)
        # log level
        self.logger.setLevel(LOGGER_LEVEL)

    def log_info(self, *args):
        self.logger.info(args[0])

# instance
# logger
logger = LoggerSHT(infoSHT.logPath, "SHT")

