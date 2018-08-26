
import unittest

import sys
sys.path.append("../sht_server")
from web3 import Web3
from time import sleep,time,mktime
import hashlib
from mongoengine import connect

from init_data import init_sht_price
from sht_server import SHTData, SHTClass
from models import *
import settings_test as sts

from config import *
from shtoken import SHToken

class TestTransferByDate(SHToken):
    def test_transferByDate(self):

        # 赎回地址账户
        fund_account = self.create_account(password)
        # 回收token账户
        collect_account = self.create_account(password)
        # 测试账户
        accounts.append(self.create_account(password))
        accounts.append(self.create_account(password))

        # 设置fund account, 设置赎回价格, 设置购买价格, 打开赎回开关
        self.set_fund_account(sts.SIBBAY_SHT_OWNER, fund_account, sts.SIBBAY_SHT_PASSWORD)
        self.set_sell_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.set_buy_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.open_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)

        # 向accounts[1]发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, accounts[1], Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        # 8.1
        print("start token_test 8.1")
        # 只有一个转账期限, 转账期限小于当前时间
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(mktime(t))
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [10*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        # 只有一个转账期限, 转账期限等于当前时间
        tsec = int(time())
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [10*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        # 只有一个转账期限, 转账期限大于当前时间
        tsec = tsec + 3600
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [10*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        # 只有一个转账期限, 转账期限大于最大时间
        tsec = tsec + 3600
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [10*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        # 只有一个转账期限, 账期限大于当前时间，小于最大时间
        tsec = tsec - 1800
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [10*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        # 清空accounts[1]可用余额
        self.transfer(accounts[1], collect_account, 20*magnitude, password, 20*magnitude)

        # 8.2
        print("start token_test 8.2.1")
        # 向accounts[1]转账10个token
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(mktime(t))
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [10*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        # 转账期限都小于当前时间
        ts = [tsec, tsec + 3600]
        vs = [1*magnitude, 2*magnitude]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 3*magnitude)
        # 转账期限一个小于当前时间，一个大于当前时间
        tsec = int(time())
        ts = [tsec - 3600, tsec + 3600]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 3*magnitude)
        # 转账期限都大于当前时间
        tsec = int(time())
        ts = [tsec + 3600, tsec + 7200]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 3*magnitude)
        # 清空accounts[1]可用余额
        self.transfer(accounts[1], collect_account, 1*magnitude, password, 1*magnitude)

        # 8.2
        print("start token_test 8.2.2")
        # 向accounts[1]转账3个token
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(mktime(t))
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [3*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 3*magnitude)
        # 转账期限都小于当前时间
        ts = [tsec, tsec + 3600]
        vs = [1*magnitude, 2*magnitude]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 3*magnitude)
        # 向accounts[1]转账3个token
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [3*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 3*magnitude)
        # 账期限一个小于当前时间，一个大于当前时间
        tsec = int(time())
        ts = [tsec - 3600, tsec + 3600]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 3*magnitude)
        # 向accounts[1]转账3个token
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [3*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 3*magnitude)
        # 转账期限都大于当前时间
        tsec = int(time())
        ts = [tsec + 3600, tsec + 7200]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 3*magnitude)

        # 8.2
        print("start token_test 8.2.3")
        # 向accounts[1]转账3个token
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(mktime(t))
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, accounts[1], [3*magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 3*magnitude)
        # 转账期限都小于当前时间
        ts = [tsec, tsec + 3600]
        vs = [20*magnitude, 20*magnitude]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 0)
        # 账期限一个小于当前时间，一个大于当前时间
        tsec = int(time())
        ts = [tsec - 3600, tsec + 3600]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 0)
        # 转账期限都大于当前时间
        tsec = int(time())
        ts = [tsec + 3600, tsec + 7200]
        self.transfer_by_date(accounts[1], accounts[2], vs, ts, password, 0)


if __name__ == '__main__':
#    connect(alias="sht", host=sts.SIBBAY_MONGODB_SHT_HOST)
    unittest.main()

