import unittest
from web3 import Web3

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestBatchTransfer(SHToken):
    def test_batch_transfer(self):

        # 赎回地址账户
        fund_account = self.create_account(config.password)
        # 回收token账户
        collect_account = self.create_account(config.password)
        # 测试账户
        test_account = self.create_account(config.password)
        # 0 地址账号
        zero_account = accounts[0]

        # 设置fund account
        self.set_fund_account(sts.SIBBAY_SHT_OWNER, fund_account, sts.SIBBAY_SHT_PASSWORD)
        # 向test_account发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 6.1-1.1
        print("start token_test 6.1-1.1")
        # 由owner向账户test_account发送10个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account], [10*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [10*config.magnitude])
        # 解冻账户test_account, 以防该账户已被冻结
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)
        # 账户test_account向账户zero_account 发送100个token
        self.batch_transfer(test_account, [zero_account], [100*config.magnitude], config.password, [0])
        # 冻结账户test_account
        self.froze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)
        # 账户test_account向账户zero_account 发送100个token
        self.batch_transfer(test_account, [zero_account], [100*config.magnitude], config.password, [0])
        # 解冻账户test_account
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)
        # 6.1-1.2
        print("start token_test 6.1-1.2")
        # 清空test_account的token
        self.clear_all_sht(test_account, collect_account, config.password)
        # 由账户test_account向collect_account发送0个token
        self.batch_transfer(test_account, [collect_account], [0], config.password, [0])
        # 由账户owner向账户test_account发送100个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account], [100*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [100*config.magnitude])
        # 由账户test_account向collect_account发送0个token
        self.batch_transfer(test_account, [collect_account], [0], config.password, [0])
        # 6.1-1.3
        print("start token_test 6.1-1.3")
        # 清空test_account的token
        self.clear_all_sht(test_account, collect_account, config.password)
        # 由账户test_account向collect_account发送1000个token
        self.batch_transfer(test_account, [collect_account], [1000*config.magnitude], config.password, [0])
        # 由账户owner向账户test_account发送100个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account], [100*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [100*config.magnitude])
        # 由账户test_account向collect_account发送1000个token
        self.batch_transfer(test_account, [collect_account], [1000*config.magnitude], config.password, [0])
        # 由账户test_account向collect_account发送2^256-1个token
        self.batch_transfer(test_account, [collect_account], [2**256-1], config.password, [0])
        # 6.1-1.4
        print("start token_test 6.1-1.4")
        # 由账户test_account向collect_account发送10个token
        self.batch_transfer(test_account, [collect_account], [10*config.magnitude], config.password, [10*config.magnitude])
        # 6.1-1.5
        print("start token_test 6.1-1.5")
        # 由账户test_account向collect_account发送所有token
        self.balance_of(test_account, 90*config.magnitude)
        self.batch_transfer(test_account, [collect_account], [90 * config.magnitude], config.password, [90 * config.magnitude])
        # 6.1-1.6
        print("start token_test 6.1-1.6")
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
        # 由账户owner向账户test_account发送110个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account], [110*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [110*config.magnitude])
        # 赎回10个token
        self.batch_transfer(test_account, [fund_account], [10*config.magnitude], config.password, [0])
        # 打开赎回开关，并分别赎回0个，10个，100个token
        self.open_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        self.batch_transfer(test_account, [fund_account], [0], config.password, [0])
        self.batch_transfer(test_account, [fund_account], [10*config.magnitude], config.password, [0])
        self.batch_transfer(test_account, [fund_account], [100*config.magnitude], config.password, [0])
        # 6.1-1.7
        print("start token_test 6.1-1.7")
        # 冻结账户test_account, 并向其转账0个token，100个token
        self.froze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account], [0], sts.SIBBAY_SHT_PASSWORD, [0])
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account], [100*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [100*config.magnitude])
        # 6.2
        print("start token_test 6.2")
        # 测试账户
        test_account_2 = self.create_account(config.password)
        test_account_3 = self.create_account(config.password)

        # 解冻账户 test_account, 清空sht，并向其转账10个token
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account, sts.SIBBAY_SHT_PASSWORD)
        self.clear_all_sht(test_account, collect_account, config.password)
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account], [10*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [10*config.magnitude])
        # 向账户 test_account_2, test_account_3 分别发送5个，6个token
        self.batch_transfer(test_account, [test_account_2, test_account_3], [5*config.magnitude, 6*config.magnitude], config.password, [0, 0])
        # 向账户 test_account_2, test_account_3 分别发送2个，3个token
        self.batch_transfer(test_account, [test_account_2, test_account_3], [2*config.magnitude, 3*config.magnitude], config.password, [2*config.magnitude, 3*config.magnitude])
        # 向账户 test_account_2, test_account_3 分别发送2个，3个token
        self.batch_transfer(test_account, [test_account_2, test_account_3], [2*config.magnitude, 3*config.magnitude], config.password, [2*config.magnitude, 3*config.magnitude])

if __name__ == '__main__':
    unittest.main()

