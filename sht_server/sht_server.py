
from sys import exit
from time import sleep

from web3 import Web3
from thread_sht import ThreadSHT
from queue import Queue
from pymongo import MongoClient
from json import loads
import settings

import requests


class SHTData:
    def __init__(self, ether_price, ether_decimals, sht_price, sht_decimals):
        self.ether_price = ether_price
        self.ether_decimals = ether_decimals
        self.sht_price = sht_price
        self.sht_decimals = sht_decimals


class SHTClass:
    def __init__(self, owner, password, contract_addr, contract_abi, sht_data, mongo_host):
        self.owner = Web3.toChecksumAddress(owner)
        self.password = password
        self.contract_addr = contract_addr
        self.contract_abi = contract_abi
        self.sht_data = sht_data
        #self.sht_queue = Queue(10000)
        self.sht_queue = Queue()
        # creat connection to mongodb
        self.conn = MongoClient(mongo_host)
        self.col_token_transfer = self.conn.sht.col_token_transfer
        self.col_token_sell = self.conn.sht.col_token_sell
        self.col_token_price = self.conn.sht.col_token_price

    def __del__(self):
        # close connection
        MongoClient.close(self.conn)

    # connect to ethereum's node
    def connect_to_node(self, node_path, timeout):
        # connect to node
        while True:
            w3 = Web3(Web3.IPCProvider(node_path))
            if w3.isConnected() == False:
                print("node is not connected, wait " + str(timeout) + " second")
                sleep(timeout)
            else:
                print("connect to node by ipc: " + node_path)
                break
        return w3

    def start_watch_sht_transfer(self, node_path, timeout):
        def handle_watch_sht_transfer(node_path, timeout):
            while self.sht_data.ether_price == 0:
                print("ether price: " + str(self.sht_data.ether_price) + "￥, wait price thread for " + str(timeout) + " seconds")
                sleep(timeout)

            # wait price thread
            w3 = self.connect_to_node(node_path, timeout)
            # get contract
            sht = w3.eth.contract(address=Web3.toChecksumAddress(self.contract_addr), abi=self.contract_abi)
            tef = sht.events.Transfer.createFilter(fromBlock='latest')
            self.loop_watch(tef, self.handle_transfer, timeout);
        t = ThreadSHT(handle_watch_sht_transfer, (node_path, timeout), self.start_watch_sht_transfer.__name__)
        t.setDaemon(True)
        t.start()
        return t

    def loop_watch(self, ef, hef, timeout):
        while True:
            for logs in ef.get_new_entries():
                hef(logs)
            print("wait event " + str(timeout) + " seconds")
            sleep(timeout)

    def handle_transfer(self, logs):
        print("transfer event from: " + logs['args']['from'] + " to: " + logs['args']['to'] + " value: " + str(logs['args']['value']))
        print("transaction hash: " + str(Web3.toHex(logs['transactionHash'])))
        # insert all transfer into collection
        msg = {"type": "TOKEN_TRANSFER",
               "from": logs['args']['from'],
               "to": logs['args']['to'],
               "value": str(logs['args']['value']),
               "transaction_hash": str(Web3.toHex(logs['transactionHash'])),
               "block_hash": str(Web3.toHex(logs['blockHash'])),
               "block_number": int(logs['blockNumber'])
              }
        self.col_token_transfer.insert_one(msg);
        # handle token sell
        if logs['args']['to'] == self.owner:
            # calcute ether value
            evalue = self.sht_data.sht_price * logs['args']['value'] * ((10**self.sht_data.ether_decimals) \
                    / (10**self.sht_data.sht_decimals)) / self.sht_data.ether_price
            msg = {"type": "TOKEN_SELL",
                   "from": logs['args']['from'],
                   "to": logs['args']['to'],
                   "value": str(logs['args']['value']),
                   "transaction_hash": str(Web3.toHex(logs['transactionHash'])),
                   "sht_price": float(self.sht_data.sht_price),
                   "ether_price": float(self.sht_data.ether_price),
                   "ether_hash": "",
                   "ether_value":str(int(evalue)),
                   "success": 0
                  }
            self.sht_queue.put(msg)
            print("put messge into SHT queue: " + str(msg))
        else:
            print("normal transfer")

    def start_queue_thread(self, timeout):
        def handle_queue(timeout):
            # get message and insert into mongodb
            while self.sht_queue.qsize() > 0:
                msg = self.sht_queue.get();
                print("get messge from SHT queue: " + str(msg))
                filter_option = {"type": "TOKEN_SELL", "transaction_hash": msg['transaction_hash']}
                ret = self.col_token_sell.find(filter_option)
                ret_count = ret.collection.count_documents(filter_option)
                if ret_count == 0:
                    self.col_token_sell.insert_one(msg);
            print("SHT queue is empty, wait " + str(timeout) + " seconds")
            sleep(timeout)

        t = ThreadSHT(handle_queue, (timeout,), self.start_queue_thread.__name__)
        t.setDaemon(True)
        t.start()
        return t

    def start_price_thread(self, timeout):
        def handle_ether_price(timeout):
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
            r = requests.get(eth_url, params = kv, timeout = timeout)
            r.raise_for_status()
            data = loads(r.text)
            #ether_price = data['ETH']['USD']
            self.sht_data.ether_price = data['ETH']['CNY']

            # update ehter Price
            filter_option = {"type": "TOKEN_PRICE"}
            ret = self.col_token_price.find(filter_option).sort('time')
            ret_count = ret.collection.count_documents(filter_option)
            latest_id = ret[ret_count-1]["_id"]
            self.col_token_price.update_one({"_id": latest_id}, {'$set': {"ether_price": float(self.sht_data.ether_price)}})

            # get latest price
            ret = self.col_token_price.find({"type": "TOKEN_PRICE"}).sort('time')
            self.sht_data.ether_price = ret[ret_count-1]["ether_price"]
            self.sht_data.ether_decimals = ret[ret_count-1]["ether_decimals"]
            self.sht_data.sht_price = ret[ret_count-1]["sht_price"]
            self.sht_data.sht_decimals = ret[ret_count-1]["sht_decimals"]

            print("get ether price: " + str(self.sht_data.ether_price) + "￥ Decimals: " + str(self.sht_data.ether_decimals) \
                  + " sht price: " + str(self.sht_data.sht_price) + "￥ Decimals: " + str(self.sht_data.sht_decimals))

            sleep(timeout)

        t = ThreadSHT(handle_ether_price, (timeout,), self.start_price_thread.__name__)
        t.setDaemon(True)
        t.start()
        return t

    # pay back ether thread
    def start_pay_ether(self, node_path, timeout):
        def handle_pay_ether(node_path, timeout):
            w3 = self.connect_to_node(node_path, timeout)
            while True:
                # find transaction
                ret = self.col_token_sell.find({"type": "TOKEN_SELL", "success": 0}).sort('time')
                for msg in ret:
                    if msg["ether_hash"] == "":
                        print("find transaction " + msg['transaction_hash'] + " needs send " + str(Web3.fromWei(int(msg['ether_value']), 'ether')) + " ether to " + msg['from'])
                        if int(msg["ether_value"]) > 0:
                            w3.personal.unlockAccount(self.owner, self.password)
                            ehash = w3.eth.sendTransaction({'from': self.owner, 'to': msg['from'], 'value': int(msg['ether_value']), 'gasPrice': 40000000000})
                            print("send ether from owner " + self.owner + ", txhash: " + str(Web3.toHex(ehash)))
                            msgid = msg["_id"]
                            self.col_token_sell.update_one({"_id": msgid}, {'$set': {"ether_hash": str(Web3.toHex(ehash))}})
                        else :
                            msgid = msg["_id"]
                            self.col_token_sell.update_one({"_id": msgid}, {'$set': {"success": int(1)}})
                    else:
                        msgid = msg["_id"]
                        ret = w3.eth.getTransaction(msg["ether_hash"])
                        if ret['blockNumber'] != None:
                            print("pay ether tx " + msg["ether_hash"] + " success")
                            self.col_token_sell.update_one({"_id": msgid}, {'$set': {"success": int(1)}})
                sleep(timeout)

        t = ThreadSHT(handle_pay_ether, (node_path, timeout), self.start_pay_ether.__name__)
        t.setDaemon(True)
        t.start()
        return t
