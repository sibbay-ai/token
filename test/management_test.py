
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

class TestTransfer(SHToken):
    def test_transfer(self):

        # 赎回地址账户
        fund_account = self.create_account(password)
        # 回收token账户
        collect_account = self.create_account(password)
        # 测试账户
        accounts.append(self.create_account(password))
        accounts.append(self.create_account(password))

        # 向 accounts[1] 发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, accounts[1], Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        # 设置fund account, 设置赎回价格, 设置购买价格, 打开赎回开关
        print("open buy sell flag")
        # 向fund account发送10 token
        self.transfer(sts.SIBBAY_SHT_OWNER, fund_account, 10*magnitude, sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        self.set_fund_account(sts.SIBBAY_SHT_OWNER, fund_account, sts.SIBBAY_SHT_PASSWORD)
        self.set_sell_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.set_buy_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.open_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)

        print("pause and unpause contract")
        # 暂停合约
        self.pause(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        # 取消暂停合约
        self.unpause(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)

        print("add administrator")
        # 添加管理员
        self.add_administrator(sts.SIBBAY_SHT_OWNER, accounts[1], sts.SIBBAY_SHT_PASSWORD)

        print("froze and unfroze account")
        # 冻结账户
        self.froze(accounts[1], accounts[2], password)
        # 解除冻结账户
        self.unfroze(accounts[1], accounts[2], password)

        print("del administrator")
        # 删除管理员
        self.del_administrator(sts.SIBBAY_SHT_OWNER, accounts[1], sts.SIBBAY_SHT_PASSWORD)

        print("send ether to contract and withdraw")
        # 向合约发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        print("buy and sell tokens")
        # 向账户accounts[1]发送 1 ether, 并购买token, 然后赎回token
        self.send_ether(sts.SIBBAY_SHT_OWNER, accounts[1], Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.buy(accounts[1], Web3.toWei(1, "ether"), password, 10*magnitude)
        self.sell(accounts[1], 10*magnitude, password, 10*magnitude)

        print("close buy sell flag")
        # 关闭赎回开关
        self.close_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        # 取回合约ether
        self.withdraw(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS)

if __name__ == '__main__':
#    connect(alias="sht", host=sts.SIBBAY_MONGODB_SHT_HOST)
    unittest.main()

