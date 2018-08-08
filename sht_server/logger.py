import logging

formatter_args = [
    '%(asctime)s','%(name)s', '%(funcName)s', '%(lineno)d', '%(levelname)s', '%(message)s'
]

formatter = logging.Formatter(' - '.join(formatter_args))
logger = logging.getLogger("sht-monitor")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.propagate = False
