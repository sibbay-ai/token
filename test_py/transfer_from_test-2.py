from web3 import Web3
import unittest

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestTransferFrom_2(SHToken):
    def test_transfer_from_2(self):
        # 赎回地址账户
        fund_account = self.create_account(config.password)
        # 回收token账户
        collect_account = self.create_account(config.password)
        # 0 地址账号
        zero_account = accounts[0]
        # 测试账户
        test_account_1 = self.create_account(config.password)
        test_account_2 = self.create_account(config.password)
        test_account_3 = self.create_account(config.password)

        # 设置fund account
        self.set_fund_account(sts.SIBBAY_SHT_OWNER, fund_account, sts.SIBBAY_SHT_PASSWORD)
        # 向 test_account_1 test_account_2 分别发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_1, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_2, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 设置代理
        self.approve(test_account_2, test_account_1, 100*config.magnitude, config.password, 100*config.magnitude)

        print("start token_test 2.2-1.1")
        # 由owner向账户 test_account_2 发送100个token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account_2, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)
        # 代理账号 test_account_1 从 账户 test_account_2 向 账户 zero_account 发送100个token
        self.transfer_from(test_account_1, test_account_2, zero_account, 100*config.magnitude, config.password, 0)

        # 冻结账户 test_account_2
        self.froze(sts.SIBBAY_SHT_OWNER, test_account_2, sts.SIBBAY_SHT_PASSWORD)
        # 代理账号 test_account_1 从 账户 test_account_2 向 账户 zero_account 发送100个token
        self.transfer_from(test_account_1, test_account_2, zero_account, 100*config.magnitude, config.password, 0)
        # 解冻账户 test_account_2
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account_2, sts.SIBBAY_SHT_PASSWORD)

        print("start token_test 2.2-1.2")
        # 设置代理
        self.approve(test_account_2, test_account_1, 0, config.password, 0)
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送0个token
        self.transfer_from(test_account_1, test_account_2, collect_account, 0, config.password, 0)
        # 设置代理
        self.approve(test_account_2, test_account_1, 100*config.magnitude, config.password, 100*config.magnitude)
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account发送0个token
        self.transfer_from(test_account_1, test_account_2, collect_account, 0, config.password, 0)

        print("start token_test 2.2-1.3")
        # 设置代理
        self.approve(test_account_2, test_account_1, 0, config.password, 0)
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送 1000 个token
        self.transfer_from(test_account_1, test_account_2, collect_account, 1000*config.magnitude, config.password, 0)
        # 设置代理
        self.approve(test_account_2, test_account_1, 100*config.magnitude, config.password, 100*config.magnitude)
        # 代理账号 test_account_1 从 账户 test_account_2 向collect_account发送1000个token
        self.transfer_from(test_account_1, test_account_2, collect_account, 1000*config.magnitude, config.password, 0)
        # 代理账号 test_account_1 从 账户 test_account_2 向collect_account发送2^256-1个token
        self.transfer_from(test_account_1, test_account_2, collect_account, 2**256-1, config.password, 0)

        print("start token_test 2.2-1.4")
        # 代理账号 test_account_1 从 账户 test_account_2 向collect_account发送10个token
        self.transfer_from(test_account_1, test_account_2, collect_account, 10*config.magnitude, config.password, 10*config.magnitude)

        print("start token_test 2.2-1.5")
        self.balance_of(test_account_2, 90*config.magnitude)
        # 代理账号 test_account_1 从 账户 test_account_2 向collect_account发送所有token
        self.transfer_from(test_account_1, test_account_2, collect_account, 90*config.magnitude, config.password, 90*config.magnitude)

        print("start token_test 2.2-1.6")
        # 关闭赎回开关
        self.close_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        #设置赎回价格
        self.set_sell_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), sts.SIBBAY_SHT_PASSWORD)
        #设置购买价格
        self.set_buy_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 取回合约所有ether
        self.withdraw(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS)
        # 向合约发送 0.1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 由账户owner向账户 test_account_2 发送110个token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account_2, 110*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 110*config.magnitude)
        # 设置代理
        self.approve(test_account_2, test_account_1, 110*config.magnitude, config.password, 110*config.magnitude)
        # 赎回10个token
        self.transfer_from(test_account_1, test_account_2, fund_account, 10*config.magnitude, config.password, 0)
        # 打开赎回开关，并分别赎回0个，10个，100个token
        self.open_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        self.transfer_from(test_account_1, test_account_2, fund_account, 0, config.password, 0)
        self.transfer_from(test_account_1, test_account_2, fund_account, 10*config.magnitude, config.password, 0)
        self.transfer_from(test_account_1, test_account_2, fund_account, 100*config.magnitude, config.password, 0)

        print("start token_test 2.2-1.7")
        # 冻结账户test_account_3, 并向其转账0个token，100个token
        self.froze(sts.SIBBAY_SHT_OWNER, test_account_3, sts.SIBBAY_SHT_PASSWORD)
        self.transfer_from(test_account_1, test_account_2, test_account_3, 0, sts.SIBBAY_SHT_PASSWORD, 0)
        self.transfer_from(test_account_1, test_account_2, test_account_3, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)

if __name__ == '__main__':
    unittest.main()

