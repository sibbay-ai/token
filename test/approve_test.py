
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
import settings_test as sts

from config import *
from shtoken import SHToken

class TestApprove(SHToken):
    def test_approve(self):

        # 赎回地址账户
        fund_account = self.create_account(password)
        # 回收token账户
        collect_account = self.create_account(password)
        # 测试账户, accounts[1] 代理， accounts[2] 被代理账户
        accounts.append(self.create_account(password))
        accounts.append(self.create_account(password))
        # 向accounts[2]发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, accounts[2], Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        # 3.1 设置代理余额为0
        print("start token_test 3.1")
        self.approve(accounts[2], accounts[1], 0, password, 0)
        # 3.2 设置代理余额为100
        print("start token_test 3.2")
        self.approve(accounts[2], accounts[1], 100*magnitude, password, 100*magnitude)
        # 3.3 设置代理余额为0
        print("start token_test 3.3")
        self.approve(accounts[2], accounts[1], 0, password, 0)

        # 4.1 提高代理额度 0
        print("start token_test 4.1")
        self.increase_approval(accounts[2], accounts[1], 0, password, 0)
        # 4.2 提高代理额度 100
        print("start token_test 4.2")
        self.increase_approval(accounts[2], accounts[1], 100*magnitude, password, 100*magnitude)
        # 4.3 提高代理额度 2^256-1
        print("start token_test 4.3")
        self.increase_approval(accounts[2], accounts[1], (2**256) - 1, password, 0)

        # 5.1 降低代理额度0
        print("start token_test 5.1")
        self.decrease_approval(accounts[2], accounts[1], 0, password, 0)
        # 5.2 降低代理额度大于0
        print("start token_test 5.2")
        self.decrease_approval(accounts[2], accounts[1], 10*magnitude, password, 10*magnitude)
        # 5.3 降低代理额度2^256-1
        print("start token_test 5.3")
        self.decrease_approval(accounts[2], accounts[1], (2**256) - 1, password, 90*magnitude)

if __name__ == '__main__':
    unittest.main()

