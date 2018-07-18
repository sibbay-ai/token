
# -*- coding: utf-8 -*-
from sys import exit
from time import sleep

from web3 import Web3
from threadSHT import ThreadSHT
from queue import Queue
from pymongo import MongoClient
from json import loads

import infoSHT
from loggerSHT import logger

import requests


#------------------------------------------------------------------------
# global

# ether price
etherPrice = 0
etherDecimals = 18

# SHT price
shtPrice = 1
shtDecimals = 0

#------------------------------------------------------------------------


class SHTClass:
    def __init__(self, owner, contractAddr, contractAbi):
        self.owner = Web3.toChecksumAddress(owner)
        self.contractAddr = contractAddr
        self.contractAbi = contractAbi
        #self.shtQueue = Queue(10000)
        self.shtQueue = Queue()

    def start_watchSHTTransfer(self, nodePath, itv):
        def handle_watchShtTransfer(nodepath, itv):
            # connect to ethereum's node
            def connectToNode(nodePath, itv):
                # connect to node
                while True:
                    w3 = Web3(Web3.IPCProvider(nodePath))
                    if w3.isConnected() == False:
                        logger.log_info("node is not connected, wait " + str(itv) + " second")
                        sleep(itv)
                    else:
                        logger.log_info("connect to node by ipc: " + nodePath)
                        break
                return w3
            # wait price thread
            global etherPrice
            while etherPrice == 0:
                logger.log_info("ether price: " + str(etherPrice) + "$, wait price thread for " + str(itv) + " seconds")
                sleep(itv)

            w3 = connectToNode(nodePath, itv)
            # get contract
            sht = w3.eth.contract(address=Web3.toChecksumAddress(self.contractAddr), abi=self.contractAbi)
            tef = sht.events.Transfer.createFilter(fromBlock='latest')
            self.loop_watch(tef, self.handle_transfer, itv);
        t = ThreadSHT(handle_watchShtTransfer, (nodePath, itv), self.start_watchSHTTransfer.__name__)
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
            evalue = shtPrice * logs['args']['value'] * ((10**etherDecimals) / (10**shtDecimals)) / etherPrice 
            msg = {"type": "sellToken",
                   "from": logs['args']['from'],
                   "to": logs['args']['to'],
                   "value": float(logs['args']['value']),
                   "thash": str(Web3.toHex(logs['transactionHash'])),
                   "tprice": float(shtPrice),
                   "eprice": float(etherPrice),
                   "ehash": "",
                   "evalue":int(evalue),
                   "success": 0
                  }
            self.shtQueue.put(msg)
            logger.log_info("put messge into SHT queue: " + str(msg))
            #logger.log_info("Should transfer back Ether to: " + logs['args']['from'])
        else:
            logger.log_info("normal transfer")

    def start_queue_thread(self, ip, port, itv):
        def handle_queue(ip, port, itv):
            # creat connection, database, collection
            conn = MongoClient(ip, port)
            shtdb = conn.sht
            shtcol = shtdb.transfer
            # get message and insert into mongodb
            while self.shtQueue.qsize() > 0:
                msg = self.shtQueue.get();
                logger.log_info("get messge from SHT queue: " + str(msg))
                ret = shtcol.find({"type": "sellToken", "thash": msg['thash']})
                if ret.count() == 0:
                    shtcol.insert(msg);
            logger.log_info("SHT queue is empty, wait " + str(itv) + " seconds")
            sleep(itv)
        t = ThreadSHT(handle_queue, (ip, port, itv), self.start_queue_thread.__name__)
        t.setDaemon(True)
        t.start()
        return t

    def start_price_thread(self, ip, port, itv):
        def handle_ether_price(ip, port, itv):
            global etherPrice
            global etherDecimals
            global shtPrice
            global shtDecimals
            eth_url="https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH&tsyms=USD"
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
            etherPrice = data['ETH']['USD']

            # creat connection, database, collection
            conn = MongoClient(ip, port)
            shtdb = conn.sht
            shtcol = shtdb.transfer
            # update ehter Price
            ret = shtcol.find({"type": "price"}).sort('time')
            latestId = ret[ret.count()-1]["_id"]
            shtcol.update({"_id": latestId}, {'$set': {"etherPrice": float(etherPrice)}})  

            # get latest price
            ret = shtcol.find({"type": "price"}).sort('time')
            etherPrice = ret[ret.count()-1]["etherPrice"]
            etherDecimals = ret[ret.count()-1]["etherDecimals"]
            shtPrice = ret[ret.count()-1]["shtPrice"]
            shtDecimals = ret[ret.count()-1]["shtDecimals"]

            logger.log_info("get ether price: " + str(etherPrice) + "$ Decimals: " + str(etherDecimals))
            logger.log_info("get sht price: " + str(shtPrice) + "$ Decimals: " + str(shtDecimals))

            sleep(itv)
        t = ThreadSHT(handle_ether_price, (ip, port, itv), self.start_price_thread.__name__)
        t.setDaemon(True)
        t.start()
        return t
    def start_pay_ether(self, nodePath, ip, port, itv):
        def handle_pay_ether(nodePath, ip, port, itv):
            # connect to ethereum's node
            def connectToNode(nodePath, itv):
                # connect to node
                while True:
                    w3 = Web3(Web3.IPCProvider(nodePath))
                    if w3.isConnected() == False:
                        logger.log_info("node is not connected, wait " + str(itv) + " second")
                        sleep(itv)
                    else:
                        logger.log_info("connect to node by ipc: " + nodePath)
                        break
                return w3
            w3 = connectToNode(nodePath, itv)
            # creat connection, database, collection
            conn = MongoClient(ip, port)
            shtdb = conn.sht
            shtcol = shtdb.transfer
            while True:
                # find transaction
                ret = shtcol.find({"type": "sellToken", "success": 0}).sort('time')
                for msg in ret:
                    if msg["ehash"] == "":
                        logger.log_info("find transaction " + msg['thash'] + " needs send " + str(Web3.fromWei(int(msg['evalue']), 'ether')) + " ether to " + msg['from'])
                        if msg["evalue"] > 0:
                            logger.log_info("send ether from owner " + self.owner)
                            w3.personal.unlockAccount(self.owner, '123456')
                            ehash = w3.eth.sendTransaction({'from': self.owner, 'to': msg['from'], 'value': int(msg['evalue']), 'gasPrice': 40000000000})
                            msgid = msg["_id"]
                            shtcol.update({"_id": msgid}, {'$set': {"ehash": str(Web3.toHex(ehash))}})
                    else:
                        msgid = msg["_id"]
                        ret = w3.eth.getTransaction(msg["ehash"])
                        if ret['blockNumber'] != None:
                            logger.log_info("pay ether tx " + msg["ehash"] + " success")
                            shtcol.update({"_id": msgid}, {'$set': {"success": int(1)}})
                sleep(itv)
        t = ThreadSHT(handle_pay_ether, (nodePath, ip, port, itv), self.start_pay_ether.__name__)
        t.setDaemon(True)
        t.start()
        return t


if __name__ == '__main__':
    sc = SHTClass(infoSHT.owner, infoSHT.address, infoSHT.abi)
    tq = sc.start_queue_thread(infoSHT.mongoDB_ip, infoSHT.mongoDB_port, 5)
    te = sc.start_price_thread(infoSHT.mongoDB_ip, infoSHT.mongoDB_port, 30)
    tw = sc.start_watchSHTTransfer(infoSHT.nodePath, 5)
    tp = sc.start_pay_ether(infoSHT.nodePath, infoSHT.mongoDB_ip, infoSHT.mongoDB_port, 5)

    tq.join()
    te.join()
    tw.join()
    tp.join()


