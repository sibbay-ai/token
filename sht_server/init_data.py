
from pymongo import MongoClient
import time
import settings

def init_sht_price(creat=False):
    # creat connection, database, collection
    conn = MongoClient(settings.SIBBAY_MONGODB_SHT_HOST)
    col_token_price = conn.sht.col_token_price

    # get price from database
    filter_option = {"type": "TOKEN_PRICE"}
    ret_count = col_token_price.collection.count_documents(filter_option)
    ret = col_token_price.find(filter_option).sort('time')
    if ret_count > 0:
        ether_price = ret[ret_count-1]["ether_price"]
    else:
        creat = True
        ether_price = settings.SIBBAY_SHT_ETHER_PRICE

    if creat == True:
        price_config = {
                "type": "TOKEN_PRICE",
                "ether_price": float(ether_price),
                "ether_decimals": int(settings.SIBBAY_SHT_ETHER_DECIMALS),
                "sht_price": float(settings.SIBBAY_SHT_SHT_PRICE),
                "sht_decimals": int(settings.SIBBAY_SHT_SHT_DECIMALS),
                "time": int(time.time())
                }
    
        # insert price config
        col_token_price.insert_one(price_config)
        print("init price ehter price: " + str(ether_price) + " decimals: " + str(settings.SIBBAY_SHT_ETHER_DECIMALS) \
              + " sht price: " + str(settings.SIBBAY_SHT_SHT_PRICE) + " decimals: " + str(settings.SIBBAY_SHT_SHT_DECIMALS))
    else:
        # update ether price
        latest_id = ret[ret_count-1]["_id"]
        col_token_price.update_one({"_id": latest_id}, {'$set': {"sht_price": float(settings.SIBBAY_SHT_SHT_PRICE)}})  
        print("update price ehter price: " + str(ether_price) + " decimals: " + str(settings.SIBBAY_SHT_ETHER_DECIMALS) \
              + " sht price: " + str(settings.SIBBAY_SHT_SHT_PRICE) + " decimals: " + str(settings.SIBBAY_SHT_SHT_DECIMALS))

    # close connection
    MongoClient.close(conn)

