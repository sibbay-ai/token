
import unittest

import sys
sys.path.append("../sht_server")
from web3 import Web3
from time import sleep,time
import hashlib
from mongoengine import connect

from init_data import init_sht_price
from sht_server import SHTData, SHTClass
from models import *
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
        sc = SHTClass(
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
        )
        self.assertEqual(sc.contract_addr, settings.SIBBAY_SHT_ADDRESS)
        self.assertEqual(sc.contract_abi, settings.SIBBAY_SHT_ABI)

    def test_connect_to_node(self):
        sht_data = SHTData(300000, 18, 1, 1)
        sc = SHTClass(
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
        )
        w3 = sc.connect_to_node(settings.SIBBAY_SHT_NODE_IPC, 5)
        self.assertEqual(w3.isConnected(), True)
        close_w3_connection(w3)

    def test_start_watch_sht_transfer(self):
        sht_data = SHTData(1000000, 18, 1, 1)
        sc = SHTClass(
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
        )
        sc.start_watch_sht_transfer(settings.SIBBAY_SHT_NODE_IPC, 5)

        # creat an event
        w3 = sc.connect_to_node(settings.SIBBAY_SHT_NODE_IPC, 5)
        self.assertEqual(w3.isConnected(), True)
        sht = w3.eth.contract(address=Web3.toChecksumAddress(settings.SIBBAY_SHT_ADDRESS), abi=settings.SIBBAY_SHT_ABI)
        w3.personal.unlockAccount(Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), settings.SIBBAY_SHT_PASSWORD)
        tx_hash = sht.functions.transfer(Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), 100).transact({"from": Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), "gasPrice": 40000000000})

        sleep(60)

        ret = TokenTransfer.query(transaction_hash = str(Web3.toHex(tx_hash)))
        self.assertEqual(ret.count(), 1)
        self.assertEqual(ret[0].from_address, Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER))
        self.assertEqual(ret[0].to_address, Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER))
        self.assertEqual(ret[0].value, '100')

        close_w3_connection(w3)

    def test_start_price_thread(self):
        init_sht_price()
        sht_data = SHTData(1000000, 18, 1, 1)
        sc = SHTClass(
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
        )
        sc.start_price_thread(sht_data, 30)

        # get price from database
        ret_count, ret = TokenPrice.query_latest_price()
        ether_price_1 = ret.ether_price


        sleep(70)

        # get price from database
        ret_count, ret = TokenPrice.query_latest_price()
        ether_price_2 = ret.ether_price

        self.assertNotEqual(ether_price_1, ether_price_2)

if __name__ == '__main__':
    connect(alias="sht", host=settings.SIBBAY_MONGODB_SHT_HOST)

    unittest.main()

