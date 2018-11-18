from web3 import Web3
import unittest

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestTransfer(SHToken):
    def test_transfer(self):

        # 回收token账户
        collect_account = self.create_account(config.password)
        # 测试账户
        test_account = self.create_account(config.password)
        # 0 地址账号
        zero_account = accounts[0]

        # 向 test_account 发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        print("start token_test 1.1.1 普通账户向0地址转账")
        # 由 owner 向账户 test_account 发送 100 个 token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)
        # 解冻账户 test_account, 以防该账户已被冻结
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)
        # 账户 test_account 向账户 zero_account 发送 100 个 token
        self.transfer(test_account, zero_account, 100*config.magnitude, config.password, 0)

        print("start token_test 1.1.2 冻结账户向0地址转账")
        # 冻结账户 test_account
        self.froze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)
        # 账户 test_account 向账户 zero_account 发送100个token
        self.transfer(test_account, zero_account, 100*config.magnitude, config.password, 100*config.magnitude)
        # 解冻账户 test_account
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)

        print("start token_test 1.2.1 当余额为0时转账0个token")
        # 清空 test_account 的 token
        self.clear_all_sht(test_account, collect_account, config.password)
        # 由账户 test_account 向 collect_account 发送 0 个 token
        self.transfer(test_account, collect_account, 0, config.password, 0)

        print("start token_test 1.2.2 当余额大于0时转账0个token")
        # 由账户 owner 向账户 test_account 发送 100 个 token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)
        # 由账户 test_account 向 collect_account 发送 0 个 token
        self.transfer(test_account, collect_account, 0, config.password, 0)

        print("start token_test 1.3.1 余额为0时，转账大于余额")
        # 清空 test_account 的 token
        self.clear_all_sht(test_account, collect_account, config.password)
        # 由账户 test_account 向 collect_account 发送 1000 个 token
        self.transfer(test_account, collect_account, 1000*config.magnitude, config.password, 0)

        print("start token_test 1.3.2 余额大于0时，转账大于余额")
        # 由账户 owner 向账户 test_account 发送 100 个 token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)
        # 由账户 test_account 向 collect_account 发送 1000 个 token
        self.transfer(test_account, collect_account, 1000*config.magnitude, config.password, 0)

        print("start token_test 1.3.3 转账2^256-1个token")
        # 由账户 test_account 向 collect_account 发送 2^256-1 个 token
        self.transfer(test_account, collect_account, 2**256-1, config.password, 0)

        print("start token_test 1.4 转账部分余额")
        self.balance_of(test_account, 100*config.magnitude)
        # 由账户 test_account 向 collect_account 发送 10 个 token
        self.transfer(test_account, collect_account, 10*config.magnitude, config.password, 10*config.magnitude)

        print("start token_test 1.5 转账所有余额")
        # 由账户 test_account 向 collect_account 发送所有 token
        self.clear_all_sht(test_account, collect_account, config.password)

        print("start token_test 1.6.1 当关闭赎回开关时，向赎回地址转账")
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
        # 由账户 owner 向账户 test_account 发送 110 个 token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account, 110*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 110*config.magnitude)
        # 赎回 10 个 token
        self.transfer(test_account, config.fund_account, 10*config.magnitude, config.password, 0)

        print("start token_test 1.6.2 当打开赎回开关时，向赎回地址转账0个token")
        # 打开赎回开关，并分别赎回 0 个，10个，100个token
        self.open_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        self.transfer(test_account, config.fund_account, 0, config.password, 0)
        self.eth_balance_of_sht_address(Web3.toWei(0.1, "ether"))

        print("start token_test 1.6.3 当打开赎回开关时，向赎回地址转账大于0个token")
        self.transfer(test_account, config.fund_account, 10*config.magnitude, config.password, 10*config.magnitude)
        self.eth_balance_of_sht_address(Web3.toWei(0.09, "ether"))

        print("start token_test 1.6.4 当打开赎回开关时，向赎回地址转账，转账赎回的金额大于合约预存金额")
        self.transfer(test_account, config.fund_account, 100*config.magnitude, config.password, 0)
        self.eth_balance_of_sht_address(Web3.toWei(0.09, "ether"))

        print("start token_test 1.7.1 向冻结账户转账0个token")
        self.froze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account, 0, sts.SIBBAY_SHT_PASSWORD, 0)

        print("start token_test 1.7.2 向冻结账户转账大于0个token")
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account, 100*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 100*config.magnitude)

if __name__ == '__main__':
    unittest.main()

