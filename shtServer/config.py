
# -*- coding: utf-8 -*-
from pymongo import MongoClient
import time
import infoSHT


# creat connection, database, collection
conn = MongoClient(infoSHT.mongoDB_ip, infoSHT.mongoDB_port)
shtdb = conn.sht
shtcol = shtdb.transfer

priceConfig = {
        "type": "price",
        "etherPrice": float(infoSHT.etherPrice),
        "etherDecimals": int(infoSHT.etherDecimals),
        "shtPrice": float(infoSHT.shtPrice),
        "shtDecimals": int(infoSHT.shtDecimals),
        "time": int(time.time())
        }

# insert price config
shtcol.insert(priceConfig)

