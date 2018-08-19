from time import sleep

from web3 import Web3
from thread_sht import ThreadSHT
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
    def __init__(self, contract_addr, contract_abi):
        self.contract_addr = Web3.toChecksumAddress(contract_addr)
        self.contract_abi = contract_abi
        self.running = True

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
            if self.running == False:
                print("stopping watch sht transfer thread....")
                exit(0)
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

    def start_price_thread(self, sht_data, timeout):
        def handle_ether_price(sht_data, timeout):
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
            sht_data.ether_price = data['ETH']['CNY']
    
            # get the latest price
            ret_count, ret = TokenPrice.query_latest_price()
            # update ether price
            ret.update(ether_price = sht_data.ether_price)
    
            # get latest price
            sht_data.ether_price = float(sht_data.ether_price)
            sht_data.ether_decimals = int(ret.ether_decimals)
            sht_data.sht_price = float(ret.sht_price)
            sht_data.sht_decimals = int(ret.sht_decimals)
    
            print("get ether price: " + str(sht_data.ether_price) + "￥ Decimals: " + str(sht_data.ether_decimals) \
                  + " sht price: " + str(sht_data.sht_price) + "￥ Decimals: " + str(sht_data.sht_decimals))
    
            if self.running == False:
                print("stopping ether price thread....")
                exit(0)
            sleep(timeout)
    
        t = ThreadSHT(handle_ether_price, (sht_data, timeout,), self.start_price_thread.__name__)
        t.setDaemon(True)
        t.start()
        return t
