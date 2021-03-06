import unittest
from web3 import Web3

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestApprove(SHToken):
    def test_approve(self):

        # 回收token账户
        collect_account = self.create_account(config.password)
        # 测试账户, test_account_1 代理， test_account_2 被代理账户
        test_account_1 = self.create_account(config.password)
        test_account_2 = self.create_account(config.password)

        # 向test_account_2发送 2 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_2, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)

        # 3.1 设置代理余额为0
        print("start token_test 3.1")
        self.approve(test_account_2, test_account_1, 0, config.password, 0)
        # 3.2 设置代理余额为100
        print("start token_test 3.2")
        self.approve(test_account_2, test_account_1, 100*config.magnitude, config.password, 100*config.magnitude)
        # 3.3 设置代理余额为0
        print("start token_test 3.3")
        self.approve(test_account_2, test_account_1, 0, config.password, 0)

        # 4.1 提高代理额度 0
        print("start token_test 4.1")
        self.increase_approval(test_account_2, test_account_1, 0, config.password, 0)
        # 4.2 提高代理额度 100
        print("start token_test 4.2")
        self.increase_approval(test_account_2, test_account_1, 100*config.magnitude, config.password, 100*config.magnitude)
        # 4.3 提高代理额度 2^256-1
        print("start token_test 4.3")
        self.increase_approval(test_account_2, test_account_1, (2**256) - 1, config.password, 0)

        # 5.1 降低代理额度0
        print("start token_test 5.1")
        self.decrease_approval(test_account_2, test_account_1, 0, config.password, 0)
        # 5.2 降低代理额度大于0
        print("start token_test 5.2")
        self.decrease_approval(test_account_2, test_account_1, 10*config.magnitude, config.password, 10*config.magnitude)
        # 5.3 降低代理额度2^256-1
        print("start token_test 5.3")
        self.decrease_approval(test_account_2, test_account_1, (2**256) - 1, config.password, 90*config.magnitude)

if __name__ == '__main__':
    unittest.main()

