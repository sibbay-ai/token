
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
            settings.SIBBAY_SHT_OWNER,
            settings.SIBBAY_SHT_PASSWORD,
            settings.SIBBAY_SHT_GAS_PRICE,
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
            sht_data,
            settings.SIBBAY_MONGODB_SHT_HOST
        )
        self.assertEqual(sc.owner, Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER))
        self.assertEqual(sc.password, settings.SIBBAY_SHT_PASSWORD)
        self.assertEqual(sc.contract_addr, settings.SIBBAY_SHT_ADDRESS)
        self.assertEqual(sc.contract_abi, settings.SIBBAY_SHT_ABI)
        self.assertEqual(sc.sht_data.ether_price, 300000)
        self.assertEqual(sc.sht_data.ether_decimals, 18)
        self.assertEqual(sc.sht_data.sht_price, 1)
        self.assertEqual(sc.sht_data.sht_decimals, 1)

    def test_connect_to_node(self):
        sht_data = SHTData(300000, 18, 1, 1)
        sc = SHTClass(
            settings.SIBBAY_SHT_OWNER,
            settings.SIBBAY_SHT_PASSWORD,
            settings.SIBBAY_SHT_GAS_PRICE,
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
            sht_data,
            settings.SIBBAY_MONGODB_SHT_HOST
        )
        w3 = sc.connect_to_node(settings.SIBBAY_SHT_NODE_IPC, 5)
        self.assertEqual(w3.isConnected(), True)
        close_w3_connection(w3)

    def test_start_watch_sht_transfer(self):
        sht_data = SHTData(1000000, 18, 1, 1)
        sc = SHTClass(
            settings.SIBBAY_SHT_OWNER,
            settings.SIBBAY_SHT_PASSWORD,
            settings.SIBBAY_SHT_GAS_PRICE,
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
            sht_data,
            settings.SIBBAY_MONGODB_SHT_HOST
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
            settings.SIBBAY_SHT_OWNER,
            settings.SIBBAY_SHT_PASSWORD,
            settings.SIBBAY_SHT_GAS_PRICE,
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
            sht_data,
            settings.SIBBAY_MONGODB_SHT_HOST
        )
        sc.start_price_thread(30)

        # get price from database
        ret_count, ret = TokenPrice.query_latest_price()
        ether_price_1 = ret.ether_price


        sleep(70)

        # get price from database
        ret_count, ret = TokenPrice.query_latest_price()
        ether_price_2 = ret.ether_price

        self.assertNotEqual(ether_price_1, ether_price_2)

    def test_start_pay_ether(self):
        sht_data = SHTData(1000000, 18, 1, 1)
        sc = SHTClass(
            settings.SIBBAY_SHT_OWNER,
            settings.SIBBAY_SHT_PASSWORD,
            settings.SIBBAY_SHT_GAS_PRICE,
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
            sht_data,
            settings.SIBBAY_MONGODB_SHT_HOST
        )
        sc.start_pay_ether(settings.SIBBAY_SHT_NODE_IPC, 5)

        tx_hash = "0x7986ab003950b4f4cfeb955a4ebe90b46df8ec15cf2f0e49939e9448a2ed0f82"

        TokenSell.query(transaction_hash = tx_hash).delete()

        TokenSell.create(
               from_address = "0x2B8edC6f7f3042893d9E93cCA6a37faB41979C16",
               to_address = "0x6D31f4bEDcE01850E4268778d1596798c5075f71",
               value = '100',
               transaction_hash = tx_hash,
               block_hash = "0x3fd8d7a7af19ba3eb2229f058e2c02059859e4b27e4211c6948a504a6c733662",
               block_number = 3669302,
               sht_price = 0.01,
               ether_price = 3211.92,
               price_unit = 'CNY',
               ether_hash = "",
               ether_value = str(311340257540661),
               status = TokenSell.STATUS__INIT
        )


        sleep(70)

        ret = TokenSell.query(transaction_hash = tx_hash)
        self.assertEqual(ret.count(), 1)
        self.assertNotEqual(ret[0].ether_hash, "")
        self.assertEqual(ret[0].status, TokenSell.STATUS__SUCCESS)


if __name__ == '__main__':
    connect(alias="sht", host=settings.SIBBAY_MONGODB_SHT_HOST)

    unittest.main()

