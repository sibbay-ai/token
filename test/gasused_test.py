
import unittest

import sys
sys.path.append("../sht_server")
from web3 import Web3
from time import sleep,time, mktime
import hashlib
from mongoengine import connect

from sht_server import SHTData, SHTClass
from models import *
import settings_test as sts

from config import *
from shtoken import SHToken

class TestGasUsed(SHToken):
    def test_gas_used(self):

        # 赎回地址账户
        fund_account = self.create_account(password)
        # 回收token账户
        collect_account = self.create_account(password)
        # 测试账户
        accounts.append(self.create_account(password))
        accounts.append(self.create_account(password))
        accounts.append(self.create_account(password))

        # 设置fund account, 设置赎回价格, 设置购买价格, 打开赎回开关
        self.set_fund_account(sts.SIBBAY_SHT_OWNER, fund_account, sts.SIBBAY_SHT_PASSWORD)
        self.set_sell_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.set_buy_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.open_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)

        # 向 accounts[1], accounts[2] 分别发送1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, accounts[1], Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.send_ether(sts.SIBBAY_SHT_OWNER, accounts[2], Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        # 由owner向账户accounts[2]发送10个token
        self.transfer(sts.SIBBAY_SHT_OWNER, accounts[2], 10*magnitude, sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        #  设置代理
        self.approve(accounts[2], accounts[1], 10*magnitude, password, 10*magnitude)

        # 创建10个账户, 10个values, 10个expects
        rs = []
        vs = []
        es = []
        for i in range(10):
            rs.append(self.create_account(password))
            vs.append((i + 1)*10000)
            es.append((i + 1)*10000)

        print("batch transfer and batch transfer from for 10 receivers")
        # batch transfer, batch transferFrom
        self.batch_transfer(accounts[2], rs, vs, password, es)
        self.batch_transfer_from(accounts[1], accounts[2], rs, vs, password, es)

        # 创建40个账户, 40个values, 40个expects
        for i in range(40):
            rs.append(self.create_account(password))
            vs.append((i + 11)*10000)
            es.append((i + 11)*10000)

        print("batch transfer and batch transfer from for 50 receivers")
        # batch transfer, batch transferFrom
        self.batch_transfer(accounts[2], rs, vs, password, es)
        self.batch_transfer_from(accounts[1], accounts[2], rs, vs, password, es)

        # 创建50个账户, 50个values, 50个expects
        for i in range(50):
            rs.append(self.create_account(password))
            vs.append((i + 51)*10000)
            es.append((i + 51)*10000)

        print("batch transfer and batch transfer from for 100 receivers")
        # batch transfer, batch transferFrom
        self.batch_transfer(accounts[2], rs, vs, password, es)
        self.batch_transfer_from(accounts[1], accounts[2], rs, vs, password, es)

        # 创建3个转账期限, 3个values, 1个expect
        ts = []
        vs = []
        ex = 0
        for i in range(3):
            t = (2018, 9, i+1, 10, 10, 30, 0, 0, 0)
            tsec = int(mktime(t))
            ts.append(tsec)
            vs.append((i + 1)*10000)
            ex = ex + ((i + 1)*10000)

        print("transfer by date and transfer from by date for 3 dates")
        # transfer by date, transfer from by date
        self.transfer_by_date(accounts[2], accounts[3], vs, ts, sts.SIBBAY_SHT_PASSWORD, ex)
        self.transfer_from_by_date(accounts[1], accounts[2], accounts[3], vs, ts, sts.SIBBAY_SHT_PASSWORD, ex)

        # 创建2个转账期限, 2个values, 2个expects
        for i in range(2):
            t = (2018, 9, i+4, 10, 10, 30, 0, 0, 0)
            tsec = int(mktime(t))
            ts.append(tsec)
            vs.append((i + 4)*10000)
            ex = ex + ((i + 4)*10000)

        print("transfer by date and transfer from by date for 5 dates")
        self.transfer_by_date(accounts[2], accounts[3], vs, ts, sts.SIBBAY_SHT_PASSWORD, ex)
        self.transfer_from_by_date(accounts[1], accounts[2], accounts[3], vs, ts, sts.SIBBAY_SHT_PASSWORD, ex)

        # 创建5个转账期限, 5个values, 5个expects
        for i in range(5):
            t = (2018, 9, i+6, 10, 10, 30, 0, 0, 0)
            tsec = int(mktime(t))
            ts.append(tsec)
            vs.append((i + 6)*10000)
            ex = ex + ((i + 6)*10000)

        print("transfer by date and transfer from by date for 10 dates")
        # transfer by date, transfer from by date
        self.transfer_by_date(accounts[2], accounts[3], vs, ts, sts.SIBBAY_SHT_PASSWORD, ex)
        self.transfer_from_by_date(accounts[1], accounts[2], accounts[3], vs, ts, sts.SIBBAY_SHT_PASSWORD, ex)


if __name__ == '__main__':
#    connect(alias="sht", host=sts.SIBBAY_MONGODB_SHT_HOST)
    unittest.main()

