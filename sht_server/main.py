
# -*- coding: utf-8 -*-
from sys import exit
from time import sleep

from web3 import Web3
from thread_sht import ThreadSHT
from queue import Queue
from pymongo import MongoClient
from json import loads

import settings
from logger_sht import logger

from init_data import init_sht_price

import requests


#------------------------------------------------------------------------
# global

# ether price
ether_price = 0
ether_decimals = 18

# SHT price
sht_price = 1
sht_decimals = 0

#------------------------------------------------------------------------


class SHTClass:
    def __init__(self, owner, password, contract_addr, contract_abi):
        self.owner = Web3.toChecksumAddress(owner)
        self.password = password
        self.contract_addr = contract_addr
        self.contract_abi = contract_abi
        #self.sht_queue = Queue(10000)
        self.sht_queue = Queue()

    # connect to ethereum's node
    def connectToNode(self, node_path, itv):
        # connect to node
        while True:
            w3 = Web3(Web3.IPCProvider(node_path))
            if w3.isConnected() == False:
                logger.log_info("node is not connected, wait " + str(itv) + " second")
                sleep(itv)
            else:
                logger.log_info("connect to node by ipc: " + node_path)
                break
        return w3

    def start_watch_sht_transfer(self, node_path, itv):
        def handle_watch_sht_transfer(node_path, itv):
            global ether_price
            while ether_price == 0:
                logger.log_info("ether price: " + str(ether_price) + "￥, wait price thread for " + str(itv) + " seconds")
                sleep(itv)

            # wait price thread
            w3 = self.connectToNode(node_path, itv)
            # get contract
            sht = w3.eth.contract(address=Web3.toChecksumAddress(self.contract_addr), abi=self.contract_abi)
            tef = sht.events.Transfer.createFilter(fromBlock='latest')
            self.loop_watch(tef, self.handle_transfer, itv);
        t = ThreadSHT(handle_watch_sht_transfer, (node_path, itv), self.start_watch_sht_transfer.__name__)
        t.setDaemon(True)
        t.start()
        return t

    def loop_watch(self, ef, hef, itv):
        while True:
            for logs in ef.get_new_entries():
                hef(logs)
            logger.log_info("wait event " + str(itv) + " seconds")
            sleep(itv)

    def handle_transfer(self, logs):
        logger.log_info("transfer event from: " + logs['args']['from'] + " to: " + logs['args']['to'] + " value: " + str(logs['args']['value']))
        logger.log_info("transaction hash: " + str(Web3.toHex(logs['transactionHash'])))
        if logs['args']['to'] == self.owner:
            # calcute ether value
            global ether_decimals
            global sht_decimals 
            evalue = sht_price * logs['args']['value'] * ((10**ether_decimals) / (10**sht_decimals)) / ether_price
            msg = {"type": "SELL_TOKEN",
                   "from": logs['args']['from'],
                   "to": logs['args']['to'],
                   "value": float(logs['args']['value']),
                   "transaction_hash": str(Web3.toHex(logs['transactionHash'])),
                   "sht_price": float(sht_price),
                   "ether_price": float(ether_price),
                   "ether_hash": "",
                   "ether_value":int(evalue),
                   "success": 0
                  }
            self.sht_queue.put(msg)
            logger.log_info("put messge into SHT queue: " + str(msg))
        else:
            logger.log_info("normal transfer")

    def start_queue_thread(self, mongo_host, itv):
        def handle_queue(mongo_host, itv):
            # creat connection, database, collection
            conn = MongoClient(mongo_host)
            sht_db = conn.sht
            sht_col = sht_db.transfer
            # get message and insert into mongodb
            while self.sht_queue.qsize() > 0:
                msg = self.sht_queue.get();
                logger.log_info("get messge from SHT queue: " + str(msg))
                ret = sht_col.find({"type": "SELL_TOKEN", "transaction_hash": msg['transaction_hash']})
                if ret.count() == 0:
                    sht_col.insert(msg);
            logger.log_info("SHT queue is empty, wait " + str(itv) + " seconds")
            sleep(itv)

        t = ThreadSHT(handle_queue, (mongo_host, itv), self.start_queue_thread.__name__)
        t.setDaemon(True)
        t.start()
        return t

    def start_price_thread(self, mongo_host, itv):
        def handle_ether_price(mongo_host, itv):
            global ether_price
            global ether_decimals
            global sht_price
            global sht_decimals
            #eth_url="https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH&tsyms=USD"
            eth_url="https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH&tsyms=CNY"
            kv = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'accept-encoding': 'gzip, deflate, br',
                  'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.5,zh;q=0.3',
                  'cache-control': 'max-age=0',
                  'host': 'min-api.cryptocompare.com',
                  'upgrade-insecure-requests': '1',
                  'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
                 }
            r = requests.get(eth_url, params = kv, timeout = itv)
            r.raise_for_status()
            data = loads(r.text)
            #ether_price = data['ETH']['USD']
            ether_price = data['ETH']['CNY']

            # creat connection, database, collection
            conn = MongoClient(mongo_host)
            sht_db = conn.sht
            sht_col = sht_db.transfer
            # update ehter Price
            ret = sht_col.find({"type": "SHT_PRICE"}).sort('time')
            latest_id = ret[ret.count()-1]["_id"]
            sht_col.update({"_id": latest_id}, {'$set': {"ether_price": float(ether_price)}})  

            # get latest price
            ret = sht_col.find({"type": "SHT_PRICE"}).sort('time')
            ether_price = ret[ret.count()-1]["ether_price"]
            ether_decimals = ret[ret.count()-1]["ether_decimals"]
            sht_price = ret[ret.count()-1]["sht_price"]
            sht_decimals = ret[ret.count()-1]["sht_decimals"]

            logger.log_info("get ether price: " + str(ether_price) + "￥ Decimals: " + str(ether_decimals))
            logger.log_info("get sht price: " + str(sht_price) + "￥ Decimals: " + str(sht_decimals))

            sleep(itv)

        t = ThreadSHT(handle_ether_price, (mongo_host, itv), self.start_price_thread.__name__)
        t.setDaemon(True)
        t.start()
        return t

    # pay back ether thread
    def start_pay_ether(self, node_path, mongo_host, itv):
        def handle_pay_ether(node_path, mongo_host, itv):
            w3 = self.connectToNode(node_path, itv)
            # creat connection, database, collection
            conn = MongoClient(mongo_host)
            sht_db = conn.sht
            sht_col = sht_db.transfer
            while True:
                # find transaction
                ret = sht_col.find({"type": "SELL_TOKEN", "success": 0}).sort('time')
                for msg in ret:
                    if msg["ether_hash"] == "":
                        logger.log_info("find transaction " + msg['transaction_hash'] + " needs send " + str(Web3.fromWei(int(msg['ether_value']), 'ether')) + " ether to " + msg['from'])
                        if msg["ether_value"] > 0:
                            logger.log_info("send ether from owner " + self.owner)
                            w3.personal.unlockAccount(self.owner, self.password)
                            ehash = w3.eth.sendTransaction({'from': self.owner, 'to': msg['from'], 'value': int(msg['ether_value']), 'gasPrice': 40000000000})
                            msgid = msg["_id"]
                            sht_col.update({"_id": msgid}, {'$set': {"ether_hash": str(Web3.toHex(ehash))}})
                        else :
                            msgid = msg["_id"]
                            sht_col.update({"_id": msgid}, {'$set': {"success": int(1)}})
                    else:
                        msgid = msg["_id"]
                        ret = w3.eth.getTransaction(msg["ether_hash"])
                        if ret['blockNumber'] != None:
                            logger.log_info("pay ether tx " + msg["ether_hash"] + " success")
                            sht_col.update({"_id": msgid}, {'$set': {"success": int(1)}})
                sleep(itv)

        t = ThreadSHT(handle_pay_ether, (node_path, mongo_host, itv), self.start_pay_ether.__name__)
        t.setDaemon(True)
        t.start()
        return t


if __name__ == '__main__':
    init_sht_price()
    sc = SHTClass(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_PASSWORD, settings.sht_address, settings.sht_abi)
    tq = sc.start_queue_thread(settings.SIBBAY_MONGODB_SHT_HOST, 5)
    te = sc.start_price_thread(settings.SIBBAY_MONGODB_SHT_HOST, 30)
    tw = sc.start_watch_sht_transfer(settings.SIBBAY_SHT_NODE_IPC, 5)
    tp = sc.start_pay_ether(settings.SIBBAY_SHT_NODE_IPC, settings.SIBBAY_MONGODB_SHT_HOST, 5)

    tq.join()
    te.join()
    tw.join()
    tp.join()


