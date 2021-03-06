import unittest
from web3 import Web3

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestManagement(SHToken):
    def test_transfer(self):

        # 回收token账户
        collect_account = self.create_account(config.password)
        # 测试账户
        test_account_1 = self.create_account(config.password)
        test_account_2 = self.create_account(config.password)

        # 向 test_account_1 发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_1, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        # 设置fund account, 设置赎回价格, 设置购买价格, 打开赎回开关
        print("open buy sell flag")
        # 向fund account发送10 token
        self.add_token_to_fund(sts.SIBBAY_SHT_OWNER, 10*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 10*config.magnitude)
        self.set_sell_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.set_buy_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.open_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        self.open_buy(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)

        print("pause and unpause contract")
        # 暂停合约
        self.pause(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        # 取消暂停合约
        self.unpause(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)

        print("add administrator")
        # 添加管理员
        self.add_administrator(sts.SIBBAY_SHT_OWNER, test_account_1, sts.SIBBAY_SHT_PASSWORD)

        print("froze and unfroze account")
        # 冻结账户
        self.froze(test_account_1, test_account_2, config.password)
        # 解除冻结账户
        self.unfroze(test_account_1, test_account_2, config.password)

        print("del administrator")
        # 删除管理员
        self.del_administrator(sts.SIBBAY_SHT_OWNER, test_account_1, sts.SIBBAY_SHT_PASSWORD)

        print("send ether to contract and withdraw")
        # 向合约发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        print("buy and sell tokens")
        # 向账户test_account_1发送 1 ether, 并购买token, 然后赎回token
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_1, Web3.toWei(2, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.buy(test_account_1, Web3.toWei(1, "ether"), config.password, 10*config.magnitude)
        self.sell(test_account_1, 10*config.magnitude, config.password, 10*config.magnitude)

        print("close buy sell flag")
        # 关闭赎回开关
        self.close_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        # 取回合约ether
        self.withdraw(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS)

if __name__ == '__main__':
    unittest.main()

