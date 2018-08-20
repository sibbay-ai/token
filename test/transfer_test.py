
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

from config import *
from shtoken import SHToken

def close_w3_connection(w3):
    w3.providers[0]._socket.sock.close()

class TestTransfer(SHToken):
    def test_transfer(self):
        # 设置fund account
        self.set_fund_account()
        # 向accounts[1]发送 0.1 ether
        self.send_ether(settings.SIBBAY_SHT_OWNER, accounts[1], Web3.toWei(0.1, "ether"), settings.SIBBAY_SHT_PASSWORD)
        # 1.1
        print("start token_test 1.1")
        # 由owner向账户accounts[1]发送100个token
        self.transfer(settings.SIBBAY_SHT_OWNER, accounts[1], 100*magnitude, settings.SIBBAY_SHT_PASSWORD, 100*magnitude)
        # 解冻账户accounts[1], 以防该账户已被冻结
        self.unfroze(settings.SIBBAY_SHT_OWNER, accounts[1], settings.SIBBAY_SHT_PASSWORD)
        # 账户accounts[1]向账户accounts[0] 发送100个token
        self.transfer(accounts[1], accounts[0], 100*magnitude, password, 0)
        # 冻结账户accounts[1]
        self.froze(settings.SIBBAY_SHT_OWNER, accounts[1], settings.SIBBAY_SHT_PASSWORD)
        # 账户accounts[1]向账户accounts[0] 发送100个token
        self.transfer(accounts[1], accounts[0], 100*magnitude, password, 100*magnitude)
        # 解冻账户accounts[1]
        self.unfroze(settings.SIBBAY_SHT_OWNER, accounts[1], settings.SIBBAY_SHT_PASSWORD)
        # 1.2
        print("start token_test 1.2")
        # 清空accounts[1]的token
        self.clear_all_sht(accounts[1])
        # 由账户accounts[1]向collect_account发送0个token
        self.transfer(accounts[1], collect_account, 0, password, 0)
        # 由账户owner向账户accounts[1]发送100个token
        self.transfer(settings.SIBBAY_SHT_OWNER, accounts[1], 100*magnitude, settings.SIBBAY_SHT_PASSWORD, 100*magnitude)
        # 由账户accounts[1]向collect_account发送0个token
        self.transfer(accounts[1], collect_account, 0, password, 0)
        # 1.3
        print("start token_test 1.3")
        # 清空accounts[1]的token
        self.clear_all_sht(accounts[1])
        # 由账户accounts[1]向collect_account发送1000个token
        self.transfer(accounts[1], collect_account, 1000*magnitude, password, 0)
        # 由账户owner向账户accounts[1]发送100个token
        self.transfer(settings.SIBBAY_SHT_OWNER, accounts[1], 100*magnitude, settings.SIBBAY_SHT_PASSWORD, 100*magnitude)
        # 由账户accounts[1]向collect_account发送1000个token
        self.transfer(accounts[1], collect_account, 1000*magnitude, password, 0)
        # 由账户accounts[1]向collect_account发送2^256-1个token
        self.transfer(accounts[1], collect_account, 2**256-1, password, 0)
        # 1.4
        print("start token_test 1.4")
        # 由账户accounts[1]向collect_account发送10个token
        self.transfer(accounts[1], collect_account, 10*magnitude, password, 10*magnitude)
        # 1.5
        print("start token_test 1.5")
        # 由账户accounts[1]向collect_account发送所有token
        self.clear_all_sht(accounts[1])
        # 1.6
        print("start token_test 1.6")
        # 关闭赎回开关
        self.close_buy_sell()
        #设置赎回价格
        self.set_sell_price(settings.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), settings.SIBBAY_SHT_PASSWORD)
        # 向合约发送 0.1 ether
        self.send_ether(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_ADDRESS, Web3.toWei(0.1, "ether"), settings.SIBBAY_SHT_PASSWORD)
        # 由账户owner向账户accounts[1]发送110个token
        self.transfer(settings.SIBBAY_SHT_OWNER, accounts[1], 110*magnitude, settings.SIBBAY_SHT_PASSWORD, 110*magnitude)
        # 赎回10个token
        self.transfer(accounts[1], fund_account, 10*magnitude, password, 0)
        # 打开赎回开关，并分别赎回0个，10个，100个token
        self.open_buy_sell()
        self.transfer(accounts[1], fund_account, 0, password, 0)
        self.transfer(accounts[1], fund_account, 10*magnitude, password, 10*magnitude)
        self.transfer(accounts[1], fund_account, 100*magnitude, password, 0)
        # 1.7
        print("start token_test 1.7")
        # 冻结账户accounts[1], 并向其转账0个token，100个token
        self.froze(settings.SIBBAY_SHT_OWNER, accounts[1], settings.SIBBAY_SHT_PASSWORD)
        self.transfer(settings.SIBBAY_SHT_OWNER, accounts[1], 0, settings.SIBBAY_SHT_PASSWORD, 0)
        self.transfer(settings.SIBBAY_SHT_OWNER, accounts[1], 100*magnitude, settings.SIBBAY_SHT_PASSWORD, 100*magnitude)

if __name__ == '__main__':
    connect(alias="sht", host=settings.SIBBAY_MONGODB_SHT_HOST)

    unittest.main()

