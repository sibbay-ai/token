
import unittest

import sys
sys.path.append("../sht_server")
from web3 import Web3
from time import sleep
from time import time
import hashlib
from pymongo import MongoClient

from init_data import init_sht_price
import sht_server
from sht_server import SHTData
from sht_server import SHTClass
import settings

def close_w3_connection(w3):
    w3.providers[0]._socket.sock.close()

class TestEventWatch(unittest.TestCase):
    def test_sht_data(self):
        sht_data = SHTData(300000, 18, 1, 1)
        self.assertEqual(sht_data.ether_price, 300000)
        self.assertEqual(sht_data.ether_decimals, 18)
        self.assertEqual(sht_data.sht_price, 1)
        self.assertEqual(sht_data.sht_decimals, 1)

    def test_sht_class(self):
        sht_data = SHTData(300000, 18, 1, 1)
        sc = SHTClass(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_PASSWORD, settings.sht_address, \
                settings.sht_abi, sht_data, settings.SIBBAY_MONGODB_SHT_HOST)
        self.assertEqual(sc.owner, Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER))
        self.assertEqual(sc.password, settings.SIBBAY_SHT_PASSWORD)
        self.assertEqual(sc.contract_addr, settings.sht_address)
        self.assertEqual(sc.contract_abi, settings.sht_abi)
        self.assertEqual(sc.sht_data.ether_price, 300000)
        self.assertEqual(sc.sht_data.ether_decimals, 18)
        self.assertEqual(sc.sht_data.sht_price, 1)
        self.assertEqual(sc.sht_data.sht_decimals, 1)

    def test_connect_to_node(self):
        sht_data = SHTData(300000, 18, 1, 1)
        sc = SHTClass(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_PASSWORD, settings.sht_address, \
                settings.sht_abi, sht_data, settings.SIBBAY_MONGODB_SHT_HOST)
        w3 = sc.connect_to_node(settings.SIBBAY_SHT_NODE_IPC, 5)
        self.assertEqual(w3.isConnected(), True)
        close_w3_connection(w3)

    def test_start_watch_sht_transfer(self):
        sht_data = SHTData(1000000, 18, 1, 1)
        sc = SHTClass(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_PASSWORD, settings.sht_address, \
                settings.sht_abi, sht_data, settings.SIBBAY_MONGODB_SHT_HOST)
        sc.start_watch_sht_transfer(settings.SIBBAY_SHT_NODE_IPC, 5)

        # creat an event
        w3 = sc.connect_to_node(settings.SIBBAY_SHT_NODE_IPC, 5)
        self.assertEqual(w3.isConnected(), True)
        sht = w3.eth.contract(address=Web3.toChecksumAddress(settings.sht_address), abi=settings.sht_abi)
        w3.personal.unlockAccount(Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), settings.SIBBAY_SHT_PASSWORD)
        tx_hash = sht.functions.transfer(Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), 100).transact({"from": Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), "gasPrice": 40000000000})

        sleep(60)
        filter_option = {"type": "TOKEN_TRANSFER", "transaction_hash": str(Web3.toHex(tx_hash))}
        ret = sc.col_token_transfer.find(filter_option)
        ret_count = ret.collection.count_documents(filter_option)
        print("tx_hash:", str(Web3.toHex(tx_hash)))
        self.assertEqual(ret_count, 1)
        self.assertEqual(ret[0]["from"], Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER))
        self.assertEqual(ret[0]["to"], Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER))
        self.assertEqual(ret[0]["value"], 100)

        close_w3_connection(w3)

    def test_start_queue_thread(self):
        sht_data = SHTData(1000000, 18, 1, 1)
        sc = SHTClass(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_PASSWORD, settings.sht_address, \
                settings.sht_abi, sht_data, settings.SIBBAY_MONGODB_SHT_HOST)
        sc.start_queue_thread(5)

        tx_hash = Web3.toHex(hashlib.sha256(bytearray("test-hash " + str(time()), "utf-8")).digest())
        msg = {"type": "TOKEN_SELL_TEST",
               "from": "0x1111111111111111111111111111111111111111",
               "to": "0x2222222222222222222222222222222222222222",
               "value": 1000000,
               "transaction_hash": str(tx_hash),
               "sht_price": 100.0,
               "ether_price": 10000.0,
               "ether_hash": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
               "ether_value": str(10000000000000000000000),
               "success": 0
              }
        sc.sht_queue.put(msg)
        sleep(10)

        filter_option = {"type": "TOKEN_SELL_TEST", "transaction_hash": str(tx_hash)}
        ret = sc.col_token_sell.find(filter_option)
        ret_count = ret.collection.count_documents(filter_option)
        self.assertEqual(ret_count, 1)
        self.assertEqual(ret[0]["from"], "0x1111111111111111111111111111111111111111")
        self.assertEqual(ret[0]["to"], "0x2222222222222222222222222222222222222222")
        self.assertEqual(ret[0]["sht_price"], 100.0)
        self.assertEqual(ret[0]["ether_price"], 10000.0)
        self.assertEqual(ret[0]["ether_value"], str(10000000000000000000000))
        self.assertEqual(ret[0]["success"], 0)

    def test_start_price_thread(self):
        init_sht_price()
        sht_data = SHTData(1000000, 18, 1, 1)
        sc = SHTClass(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_PASSWORD, settings.sht_address, \
                settings.sht_abi, sht_data, settings.SIBBAY_MONGODB_SHT_HOST)
        sc.start_price_thread(30)

        # get price from database
        filter_option = {"type": "TOKEN_PRICE"}
        ret = sc.col_token_price.find(filter_option).sort('time')
        ret_count = ret.collection.count_documents(filter_option)
        ether_price_1 = ret[ret_count-1]["ether_price"]

        sleep(70)

        # get price from database
        ret = sc.col_token_price.find(filter_option).sort('time')
        ether_price_2 = ret[ret_count-1]["ether_price"]
        self.assertNotEqual(ether_price_1, ether_price_2)

    def test_start_pay_ether(self):
        sht_data = SHTData(1000000, 18, 1, 1)
        sc = SHTClass(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_PASSWORD, settings.sht_address, \
                settings.sht_abi, sht_data, settings.SIBBAY_MONGODB_SHT_HOST)
        sc.start_pay_ether(settings.SIBBAY_SHT_NODE_IPC, 5)

        tx_hash = "0x7986ab003950b4f4cfeb955a4ebe90b46df8ec15cf2f0e49939e9448a2ed0f82"

        msg = {"type" : "TOKEN_SELL",
               "from" : "0x2B8edC6f7f3042893d9E93cCA6a37faB41979C16",
               "to" : "0x6D31f4bEDcE01850E4268778d1596798c5075f71",
               "value" : 100,
               "transaction_hash" : tx_hash,
               "sht_price" : 0.01,
               "ether_price" : 3211.92,
               "ether_hash" : "",
               "ether_value" : str(311340257540661),
               "success" : 0
               }

        filter_option = {"type": "TOKEN_SELL", "transaction_hash": tx_hash}
        sc.col_token_sell.delete_one(filter_option)
        sc.col_token_sell.insert_one(msg);

        sleep(70)

        ret = sc.col_token_sell.find(filter_option)
        ret_count = ret.collection.count_documents(filter_option)
        self.assertEqual(ret_count, 1)
        self.assertNotEqual(ret[0]["ether_hash"], "")
        self.assertEqual(ret[0]["success"], 1)


if __name__ == '__main__':
    unittest.main()
