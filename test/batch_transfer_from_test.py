
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
        accounts.append(self.create_account(password))
        accounts.append(self.create_account(password))

        # 设置fund account
        self.set_fund_account(sts.SIBBAY_SHT_OWNER, fund_account, sts.SIBBAY_SHT_PASSWORD)
        # 向accounts[1], accounts[2]分别发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, accounts[1], Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.send_ether(sts.SIBBAY_SHT_OWNER, accounts[2], Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 7.1-1.1
        print("start token_test 7.1-1.1")
        # 由owner向账户accounts[2]发送10个token
        self.transfer(sts.SIBBAY_SHT_OWNER, accounts[2], 10*magnitude, sts.SIBBAY_SHT_PASSWORD, 10*magnitude)
        # 设置账户accounts[1]代理账户accounts[2]
        self.approve(accounts[2], accounts[1], 10*magnitude, password, 10*magnitude)
        # 账户accounts[2]向账户accounts[0] 发送10个token
        self.batch_transfer_from(accounts[1], accounts[2], [accounts[0]], [10*magnitude], password, [0])
        # 冻结账户accounts[1]
        self.froze(sts.SIBBAY_SHT_OWNER, accounts[1], sts.SIBBAY_SHT_PASSWORD)
        # 账户accounts[1]向账户accounts[0] 发送10个token
        self.batch_transfer_from(accounts[1], accounts[2], [accounts[0]], [10*magnitude], password, [0])
        # 解冻账户accounts[1]
        self.unfroze(sts.SIBBAY_SHT_OWNER, accounts[1], sts.SIBBAY_SHT_PASSWORD)
        # 清空accounts[2]的token
        self.clear_all_sht(accounts[2], collect_account, password)
        # 7.1-1.2
        print("start token_test 7.1-1.2")
        # 设置代理额度为0
        self.approve(accounts[2], accounts[1], 0, password, 0)
        # 由账户accounts[2]向collect_account发送0个token
        self.batch_transfer_from(accounts[1], accounts[2], [collect_account], [0], password, [0])
        # 由账户owner向账户accounts[2]发送10个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [accounts[2]], [10*magnitude], sts.SIBBAY_SHT_PASSWORD, [10*magnitude])
        # 设置代理额度为10
        self.approve(accounts[2], accounts[1], 10*magnitude, password, 10*magnitude)
        # 由账户accounts[2]向collect_account发送0个token
        self.batch_transfer_from(accounts[1], accounts[2], [collect_account], [0], password, [0])
        # 清空accounts[2]的token
        self.clear_all_sht(accounts[2], collect_account, password)
        # 7.1-1.3
        print("start token_test 7.1-1.3")
        # 由账户owner向账户accounts[2]发送10个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [accounts[2]], [10*magnitude], sts.SIBBAY_SHT_PASSWORD, [10*magnitude])
        # 设置代理额度为0
        self.approve(accounts[2], accounts[1], 0, password, 0)
        # 由账户accounts[2]向collect_account发送100个token
        self.batch_transfer_from(accounts[1], accounts[2], [collect_account], [100*magnitude], password, [0])
        # 设置代理额度为10
        self.approve(accounts[2], accounts[1], 10*magnitude, password, 10*magnitude)
        # 由账户accounts[2]向collect_account发送1000个token
        self.batch_transfer_from(accounts[1], accounts[2], [collect_account], [100*magnitude], password, [0])
        # 由账户accounts[2]向collect_account发送2^256-1个token
        self.batch_transfer_from(accounts[1], accounts[2], [collect_account], [2**256-1], password, [0])
        # 7.1-1.4
        print("start token_test 7.1-1.4")
        # 由账户accounts[1]向collect_account发送2个token
        self.batch_transfer_from(accounts[1], accounts[2], [collect_account], [2*magnitude], password, [2*magnitude])
        # 7.1-1.5
        print("start token_test 7.1-1.5")
        # 由账户accounts[1]向collect_account发送所有token
        self.batch_transfer_from(accounts[1], accounts[2], [collect_account], [8*magnitude], password, [8*magnitude])
        # 7.1-1.6
        print("start token_test 7.1-1.6")
        # 关闭赎回开关
        self.close_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        #设置赎回价格
        self.set_sell_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), sts.SIBBAY_SHT_PASSWORD)
        #设置购买价格
        self.set_buy_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 取回合约所有ether
        self.withdraw(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS)
        # 向合约发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 由账户owner向账户accounts[2]发送10个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [accounts[2]], [110*magnitude], sts.SIBBAY_SHT_PASSWORD, [110*magnitude])
        # 设置代理额度为10
        self.approve(accounts[2], accounts[1], 110*magnitude, password, 110*magnitude)
        # 赎回10个token
        self.batch_transfer_from(accounts[1], accounts[2], [fund_account], [10*magnitude], password, [0])
        # 打开赎回开关，并分别赎回0个，10个，100个token
        self.open_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        self.batch_transfer_from(accounts[1], accounts[2], [fund_account], [0], password, [0])
        self.batch_transfer_from(accounts[1], accounts[2], [fund_account], [10*magnitude], password, [0])
        self.batch_transfer_from(accounts[1], accounts[2], [fund_account], [100*magnitude], password, [0])
        # 7.1-1.7
        print("start token_test 7.1-1.7")
        # 冻结账户accounts[3], 并向其转账0个token，10个token
        self.froze(sts.SIBBAY_SHT_OWNER, accounts[3], sts.SIBBAY_SHT_PASSWORD)
        self.batch_transfer_from(accounts[1], accounts[2], [accounts[3]], [0], password, [0])
        self.batch_transfer_from(accounts[1], accounts[2], [accounts[3]], [10*magnitude], password, [10*magnitude])
        # 7.2
        print("start token_test 7.2")
        # 设置代理额度为10
        self.approve(accounts[2], accounts[1], 10*magnitude, password, 10*magnitude)
        # 向账户 accounts[3], accounts[4] 分别发送5个，6个token
        self.batch_transfer_from(accounts[1], accounts[2], [accounts[3], accounts[4]], [5*magnitude, 6*magnitude], password, [0, 0])
        # 向账户 accounts[3], accounts[4] 分别发送2个，3个token
        self.batch_transfer_from(accounts[1], accounts[2], [accounts[3], accounts[4]], [2*magnitude, 3*magnitude], password, [2*magnitude, 3*magnitude])
        # 向账户 accounts[3], accounts[4] 分别发送2个，3个token
        self.batch_transfer_from(accounts[1], accounts[2], [accounts[3], accounts[4]], [2*magnitude, 3*magnitude], password, [2*magnitude, 3*magnitude])

if __name__ == '__main__':
#    connect(alias="sht", host=sts.SIBBAY_MONGODB_SHT_HOST)
    unittest.main()

