import time

from web3 import Web3
import unittest

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestTransferFromByDate(SHToken):
    def test_transferFromByDate(self):

        # 回收token账户
        collect_account = self.create_account(config.password)
        # 测试账户
        test_account_1 = self.create_account(config.password)
        test_account_2 = self.create_account(config.password)
        test_account_3 = self.create_account(config.password)

        # 设置fund account, 设置赎回价格, 设置购买价格, 打开赎回开关
        self.set_sell_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.set_buy_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.open_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)

        # 向test_account_1发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_1, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_2, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        # 向test_account_2转账100个token
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(time.mktime(t))
        self.transfer_by_date(sts.SIBBAY_SHT_OWNER, test_account_2, [100*config.magnitude], [tsec], sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)
        # 9.1
        print("start token_test 9.1")
        # 代理余额为0
        self.approve(test_account_2, test_account_1, 0, config.password, 0)
        # 只有一个转账期限, 转账期限小于当前时间
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(time.mktime(t))
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [10*config.magnitude], [tsec], config.password, 0)
        # 只有一个转账期限, 转账期限等于当前时间
        tsec = int(time.time())
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [10*config.magnitude], [tsec], config.password, 0)
        # 只有一个转账期限, 转账期限大于当前时间
        tsec = tsec + 3600
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [10*config.magnitude], [tsec], config.password, 0)
        # 只有一个转账期限, 转账期限大于最大时间
        tsec = tsec + 3600
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [10*config.magnitude], [tsec], config.password, 0)
        # 只有一个转账期限, 账期限大于当前时间，小于最大时间
        tsec = tsec - 1800
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [10*config.magnitude], [tsec], config.password, 0)

        # 9.2-9.1
        print("start token_test 9.2-9.1")
        # 代理余额为10
        self.approve(test_account_2, test_account_1, 10*config.magnitude, config.password, 10*config.magnitude)
        # 只有一个转账期限, 转账期限小于当前时间
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(time.mktime(t))
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [1*config.magnitude], [tsec], config.password, 1*config.magnitude)
        # 只有一个转账期限, 转账期限等于当前时间
        tsec = int(time.time())
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [1*config.magnitude], [tsec], config.password, 1*config.magnitude)
        # 只有一个转账期限, 转账期限大于当前时间
        tsec = tsec + 3600
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [1*config.magnitude], [tsec], config.password, 1*config.magnitude)
        # 只有一个转账期限, 转账期限大于最大时间
        tsec = tsec + 3600
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [1*config.magnitude], [tsec], config.password, 1*config.magnitude)
        # 只有一个转账期限, 账期限大于当前时间，小于最大时间
        tsec = tsec - 1800
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, [1*config.magnitude], [tsec], config.password, 1*config.magnitude)

        # 9.2-8.2
        print("start token_test 9.2-8.2.1")
        # 代理余额为10
        self.approve(test_account_2, test_account_1, 10*config.magnitude, config.password, 10*config.magnitude)
        # 转账期限都小于当前时间
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(time.mktime(t))
        ts = [tsec, tsec + 3600]
        vs = [1*config.magnitude, 2*config.magnitude]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 3*config.magnitude)
        # 转账期限一个小于当前时间，一个大于当前时间
        tsec = int(time.time())
        ts = [tsec - 3600, tsec + 3600]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 3*config.magnitude)
        # 转账期限都大于当前时间
        tsec = int(time.time())
        ts = [tsec + 3600, tsec + 7200]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 3*config.magnitude)

        # 9.2-8.2
        print("start token_test 9.2-8.2.2")
        # 代理余额为3
        self.approve(test_account_2, test_account_1, 3*config.magnitude, config.password, 3*config.magnitude)
        # 转账期限都小于当前时间
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(time.mktime(t))
        ts = [tsec, tsec + 3600]
        vs = [1*config.magnitude, 2*config.magnitude]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 3*config.magnitude)
        # 代理余额为3
        self.approve(test_account_2, test_account_1, 3*config.magnitude, config.password, 3*config.magnitude)
        # 账期限一个小于当前时间，一个大于当前时间
        tsec = int(time.time())
        ts = [tsec - 3600, tsec + 3600]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 3*config.magnitude)
        # 代理余额为3
        self.approve(test_account_2, test_account_1, 3*config.magnitude, config.password, 3*config.magnitude)
        # 转账期限都大于当前时间
        tsec = int(time.time())
        ts = [tsec + 3600, tsec + 7200]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 3*config.magnitude)

        # 9.2-8.2
        print("start token_test 9.2-8.2.3")
        # 代理余额为3
        self.approve(test_account_2, test_account_1, 3*config.magnitude, config.password, 3*config.magnitude)
        # 转账期限都小于当前时间
        t = (2018, 8, 1, 10, 10, 30, 0, 0, 0)
        tsec = int(time.mktime(t))
        ts = [tsec, tsec + 3600]
        vs = [20*config.magnitude, 20*config.magnitude]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 0)
        # 账期限一个小于当前时间，一个大于当前时间
        tsec = int(time.time())
        ts = [tsec - 3600, tsec + 3600]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 0)
        # 转账期限都大于当前时间
        tsec = int(time.time())
        ts = [tsec + 3600, tsec + 7200]
        self.transfer_from_by_date(test_account_1, test_account_2, test_account_3, vs, ts, config.password, 0)


if __name__ == '__main__':
    unittest.main()

