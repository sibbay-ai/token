from web3 import Web3
import unittest

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestTransferFrom_1(SHToken):
    def test_transfer_from_1(self):
        # 回收token账户
        collect_account = self.create_account(config.password)
        # 0 地址账号
        zero_account = accounts[0]
        # 测试账户
        test_account_1 = self.create_account(config.password)
        test_account_2 = self.create_account(config.password)
        test_account_3 = self.create_account(config.password)

        # 解冻账户 test_account_1 test_account_2, 以防该账户已被冻结
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account_1, sts.SIBBAY_SHT_PASSWORD)
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account_2, sts.SIBBAY_SHT_PASSWORD)
        # 设置代理 test_account_1 成为 test_account_2 的代理，额度为 0
        self.approve(test_account_2, test_account_1, 0, config.password, 0)
        # 向 test_account_1 发送 3 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_1, Web3.toWei(3, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 向 test_account_2 发送 3 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_2, Web3.toWei(3, "ether"), sts.SIBBAY_SHT_PASSWORD)

        print("start token_test 2.1 - 1.1.1 代理余额为0，普通账户向0地址转账 ")
        # 由 owner 向账户 test_account_2 发送 100 个token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account_2, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)
        # 代理账号 test_account_1 从 账户 test_account_2 向账户 zero_account 发送 100 个 token
        self.transfer_from(test_account_1, test_account_2, zero_account, 100*config.magnitude, config.password, 0)

        print("start token_test 2.1 - 1.1.2 代理余额为0，冻结账户向0地址转账 ")
        # 冻结账户 test_account_2
        self.froze(sts.SIBBAY_SHT_OWNER, test_account_2, sts.SIBBAY_SHT_PASSWORD)
        # 代理账号 test_account_1 从 账户 test_account_2 向账户 zero_account 发送 100 个 token
        self.transfer_from(test_account_1, test_account_2, zero_account, 100*config.magnitude, config.password, 0)
        # 解冻账户 test_account_2
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account_2, sts.SIBBAY_SHT_PASSWORD)

        print("start token_test 2.1 - 1.2.2 代理余额为0，余额大于0时转账0个token")
        self.balance_of(test_account_2, 100*config.magnitude)
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送0个token
        self.transfer_from(test_account_1, test_account_2, collect_account, 0, config.password, 0)

        print("start token_test 2.1 - 1.2.1 代理余额为0，余额为0时转账0个token")
        # 清空 test_account_2 的 token
        self.clear_all_sht(test_account_2, collect_account, config.password)
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送 0 个 token
        self.transfer_from(test_account_1, test_account_2, collect_account, 0, config.password, 0)

        print("start token_test 2.1 - 1.3.1 代理余额为0，余额为0时，转账大于余额")
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送 1000 个 token
        self.transfer_from(test_account_1, test_account_2, collect_account, 1000*config.magnitude, config.password, 0)

        print("start token_test 2.1 - 1.3.2 代理余额为0，余额大于0时，转账大于余额")
        # 由账户 owner 向账户 test_account_2 发送 100 个 token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account_2, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送 1000 个 token
        self.transfer_from(test_account_1, test_account_2, collect_account, 1000*config.magnitude, config.password, 0)

        print("start token_test 2.1 - 1.3.3 代理余额为0，余额大于0时，转账2^256-1个token")
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送2^256-1个token
        self.transfer_from(test_account_1, test_account_2, collect_account, 2**256-1, config.password, 0)

        print("start token_test 2.1 - 1.4 代理余额为0，转账部分余额")
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送 10 个 token
        self.transfer_from(test_account_1, test_account_2, collect_account, 10*config.magnitude, config.password, 0)

        print("start token_test 2.1 - 1.5 代理余额为0，转账所有余额")
        # 代理账号 test_account_1 从 账户 test_account_2 向 collect_account 发送所有token
        self.transfer_from(test_account_1, test_account_2, collect_account, 90*config.magnitude, config.password, 0)

        print("start token_test 2.1 - 1.6.1 代理余额为0，当关闭赎回开关时，向赎回地址转账")
        # 关闭赎回开关
        self.close_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        #设置赎回价格
        self.set_sell_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.001, "ether"), sts.SIBBAY_SHT_PASSWORD)
        #设置购买价格
        self.set_buy_price(sts.SIBBAY_SHT_OWNER, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 取回合约所有ether
        self.withdraw(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS)
        # 向合约发送 0.1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_ADDRESS, Web3.toWei(0.1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        self.balance_of(test_account_2, 100*config.magnitude)
        # 赎回10个token
        self.transfer_from(test_account_1, test_account_2, config.fund_account, 10*config.magnitude, config.password, 0)

        print("start token_test 2.1 - 1.6.2 代理余额为0，当打开赎回开关时，向赎回地址转账0个token")
        # 打开赎回开关，并分别赎回0个，10个，100个token
        self.open_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        self.transfer_from(test_account_1, test_account_2, config.fund_account, 0, config.password, 0)

        print("start token_test 2.1 - 1.6.3 代理余额为0，当打开赎回开关时，向赎回地址转账大于0个token")
        self.transfer_from(test_account_1, test_account_2, config.fund_account, 10*config.magnitude, config.password, 0)

        print("start token_test 2.1 - 1.6.4 代理余额为0，当打开赎回开关时，向赎回地址转账，转账赎回的金额大于合约预存金额")
        self.transfer_from(test_account_1, test_account_2, config.fund_account, 110*config.magnitude, config.password, 0)

        print("start token_test 2.1 - 1.7.1 代理余额为0，向冻结账户转账0个token")
        # 冻结账户 test_account_3, 并向其转账 0 个token
        self.froze(sts.SIBBAY_SHT_OWNER, test_account_3, sts.SIBBAY_SHT_PASSWORD)
        self.transfer_from(test_account_1, test_account_2, test_account_3, 0, sts.SIBBAY_SHT_PASSWORD, 0)

        print("start token_test 2.1 - 1.7.2 代理余额为0，向冻结账户转账大于0个token")
        # 冻结账户 test_account_3, 并向其转账 100 个token
        self.transfer_from(test_account_1, test_account_2, test_account_3, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 0)

if __name__ == '__main__':
    unittest.main()

