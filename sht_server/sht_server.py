from time import sleep

from web3 import Web3
from thread_sht import ThreadSHT
from queue import Queue
from pymongo import MongoClient
from json import loads

import requests

from models import *


class SHTData:
    def __init__(self, ether_price, ether_decimals, sht_price, sht_decimals):
        self.ether_price = ether_price
        self.ether_decimals = ether_decimals
        self.sht_price = sht_price
        self.sht_decimals = sht_decimals


class SHTClass:
    def __init__(self, owner, password, gas_price, contract_addr, contract_abi, sht_data, mongo_host):
        self.owner = Web3.toChecksumAddress(owner)
        self.password = password
        self.gas_price = gas_price
        self.contract_addr = contract_addr
        self.contract_abi = contract_abi
        self.sht_data = sht_data
        #self.sht_queue = Queue(10000)
        self.sht_queue = Queue()

    def __del__(self):
        pass

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
        # insert all transfer into collection
        ret = TokenTransfer.query(transaction_hash = str(Web3.toHex(logs['transactionHash'])))
        if ret.count() == 0:
            TokenTransfer.create(
                   from_address = logs['args']['from'],
                   to_address = logs['args']['to'],
                   value = str(logs['args']['value']),
                   transaction_hash = str(Web3.toHex(logs['transactionHash'])),
                   block_hash = str(Web3.toHex(logs['blockHash'])),
                   block_number = int(logs['blockNumber'])
            )

        # handle token sell
        if logs['args']['to'] == self.owner:
            ret = TokenSell.query(transaction_hash = str(Web3.toHex(logs['transactionHash'])))

            if ret.count() == 0:
                # calcute ether value
                evalue = self.sht_data.sht_price * logs['args']['value'] * ((10**self.sht_data.ether_decimals) \
                        / (10**self.sht_data.sht_decimals)) / self.sht_data.ether_price

                TokenSell.create(
                       from_address = logs['args']['from'],
                       to_address = logs['args']['to'],
                       value = str(logs['args']['value']),
                       transaction_hash = str(Web3.toHex(logs['transactionHash'])),
                       block_hash = str(Web3.toHex(logs['blockHash'])),
                       block_number = int(logs['blockNumber']),
                       sht_price = float(self.sht_data.sht_price),
                       ether_price = float(self.sht_data.ether_price),
                       price_unit = 'CNY',
                       ether_hash = "",
                       ether_value = str(int(evalue)),
                       status = TokenSell.STATUS__INIT
                )

                print("find token sell:")
                print("from: " + logs['args']['from'] + " to: " + logs['args']['to'] + " value: " + str(logs['args']['value']))
                print("transaction hash: " + str(Web3.toHex(logs['transactionHash'])))

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

            # get the latest price
            ret_count, ret = TokenPrice.query_latest_price()
            # update ether price
            ret.update(ether_price = self.sht_data.ether_price)

            # get latest price
            self.sht_data.ether_price = float(ret.ether_price)
            self.sht_data.ether_decimals = int(ret.ether_decimals)
            self.sht_data.sht_price = float(ret.sht_price)
            self.sht_data.sht_decimals = int(ret.sht_decimals)

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
                rets = TokenSell.query(status = TokenSell.STATUS__INIT)
                for ret in rets:
                    ret.update(status = TokenSell.STATUS__PROCESSING)
                    if int(ret.ether_value) > 0:
                        w3.personal.unlockAccount(self.owner, self.password)
                        ehash = w3.eth.sendTransaction({'from': self.owner, 'to': ret.from_address, 'value': int(ret.ether_value), 'gasPrice': int(self.gas_price)})
                        print("send ether from owner " + self.owner + ", txhash: " + str(Web3.toHex(ehash)))
                        ret.update(ether_hash = str(Web3.toHex(ehash)))
                    else :
                        ret.update(status = TokenSell.STATUS__SUCCESS)

                # check status
                rets = TokenSell.query(status = TokenSell.STATUS__PROCESSING)
                for ret in rets:
                    if ret.ether_hash != "":
                        logs = w3.eth.getTransaction(ret.ether_hash)
                        if logs['blockNumber'] != None:
                            print("pay ether tx " + ret.ether_hash + " success")
                            ret.update(status = TokenSell.STATUS__SUCCESS)
                sleep(timeout)

        t = ThreadSHT(handle_pay_ether, (node_path, timeout), self.start_pay_ether.__name__)
        t.setDaemon(True)
        t.start()
        return t
