
import time
import settings

from mongoengine import connect
from models import TokenPrice
from .logger import logger


def init_sht_price(creat=False):
    # creat connection, database, collection
    connect(alias="sht", host=settings.SIBBAY_MONGODB_SHT_HOST)

    # get the latest price
    ret_count, ret = TokenPrice.query_latest_price()
    if ret_count > 0:
        ether_price = ret.ether_price
    else:
        creat = True
        ether_price = settings.SIBBAY_ETHER_PRICE

    if creat == True:
        TokenPrice.create(
                ether_price = float(ether_price),
                ether_decimals = int(settings.SIBBAY_ETHER_DECIMALS),
                sht_price = float(settings.SIBBAY_SHT_PRICE),
                sht_decimals = int(settings.SIBBAY_SHT_DECIMALS),
                price_unit = "CNY"
        )

        logger.info("init price ehter price: " + str(ether_price) + " decimals: " + str(settings.SIBBAY_ETHER_DECIMALS) \
              + " sht price: " + str(settings.SIBBAY_SHT_PRICE) + " decimals: " + str(settings.SIBBAY_SHT_DECIMALS))
    else:
        # update sht price
        ret.update(sht_price = float(settings.SIBBAY_SHT_PRICE))
        logger.info("update price ehter price: " + str(ether_price) + " decimals: " + str(settings.SIBBAY_ETHER_DECIMALS) \
              + " sht price: " + str(settings.SIBBAY_SHT_PRICE) + " decimals: " + str(settings.SIBBAY_SHT_DECIMALS))

