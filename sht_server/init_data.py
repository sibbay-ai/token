
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import time
import settings

def init_sht_price():
    # creat connection, database, collection
    conn = MongoClient(settings.SIBBAY_MONGODB_SHT_HOST)
    sht_db = conn.sht
    sht_col = sht_db.transfer

    # get price from database
    ret = sht_col.find({"type": "SHT_PRICE"}).sort('time')
    if ret.count() > 0:
        ether_price = ret[ret.count()-1]["ether_price"]
    else:
        ether_price = settings.SIBBAY_SHT_ETHER_PRICE
    
    price_config = {
            "type": "SHT_PRICE",
            "ether_price": float(ether_price),
            "ether_decimals": int(settings.SIBBAY_SHT_ETHER_DECIMALS),
            "sht_price": float(settings.SIBBAY_SHT_SHT_PRICE),
            "sht_decimals": int(settings.SIBBAY_SHT_SHT_DECIMALS),
            "time": int(time.time())
            }
    
    # insert price config
    sht_col.insert(price_config)

