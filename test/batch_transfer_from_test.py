import unittest
from web3 import Web3

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestBatchTransferFrom(SHToken):
    def test_transfer(self):

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
        test_account_4 = self.create_account(config.password)

        # 设置fund account
        self.set_fund_account(sts.SIBBAY_SHT_OWNER, fund_account, sts.SIBBAY_SHT_PASSWORD)
        # 向test_account_1, test_account_2分别发送 1 ether
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_1, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        self.send_ether(sts.SIBBAY_SHT_OWNER, test_account_2, Web3.toWei(1, "ether"), sts.SIBBAY_SHT_PASSWORD)
        # 7.1-1.1
        print("start token_test 7.1-1.1")
        # 由owner向账户test_account_2发送10个token
        self.transfer(sts.SIBBAY_SHT_OWNER, test_account_2, 10*config.magnitude, sts.SIBBAY_SHT_PASSWORD, 10*config.magnitude)
        # 设置账户test_account_1代理账户test_account_2
        self.approve(test_account_2, test_account_1, 10*config.magnitude, config.password, 10*config.magnitude)
        # 账户test_account_2向账户zero_account 发送10个token
        self.batch_transfer_from(test_account_1, test_account_2, [zero_account], [10*config.magnitude], config.password, [0])
        # 冻结账户test_account_1
        self.froze(sts.SIBBAY_SHT_OWNER, test_account_1, sts.SIBBAY_SHT_PASSWORD)
        # 账户test_account_1向账户zero_account 发送10个token
        self.batch_transfer_from(test_account_1, test_account_2, [zero_account], [10*config.magnitude], config.password, [0])
        # 解冻账户test_account_1
        self.unfroze(sts.SIBBAY_SHT_OWNER, test_account_1, sts.SIBBAY_SHT_PASSWORD)
        # 清空test_account_2的token
        self.clear_all_sht(test_account_2, collect_account, config.password)
        # 7.1-1.2
        print("start token_test 7.1-1.2")
        # 设置代理额度为0
        self.approve(test_account_2, test_account_1, 0, config.password, 0)
        # 由账户test_account_2向collect_account发送0个token
        self.batch_transfer_from(test_account_1, test_account_2, [collect_account], [0], config.password, [0])
        # 由账户owner向账户test_account_2发送10个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account_2], [10*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [10*config.magnitude])
        # 设置代理额度为10
        self.approve(test_account_2, test_account_1, 10*config.magnitude, config.password, 10*config.magnitude)
        # 由账户test_account_2向collect_account发送0个token
        self.batch_transfer_from(test_account_1, test_account_2, [collect_account], [0], config.password, [0])
        # 清空test_account_2的token
        self.clear_all_sht(test_account_2, collect_account, config.password)
        # 7.1-1.3
        print("start token_test 7.1-1.3")
        # 由账户owner向账户test_account_2发送10个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account_2], [10*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [10*config.magnitude])
        # 设置代理额度为0
        self.approve(test_account_2, test_account_1, 0, config.password, 0)
        # 由账户test_account_2向collect_account发送100个token
        self.batch_transfer_from(test_account_1, test_account_2, [collect_account], [100*config.magnitude], config.password, [0])
        # 设置代理额度为10
        self.approve(test_account_2, test_account_1, 10*config.magnitude, config.password, 10*config.magnitude)
        # 由账户test_account_2向collect_account发送1000个token
        self.batch_transfer_from(test_account_1, test_account_2, [collect_account], [100*config.magnitude], config.password, [0])
        # 由账户test_account_2向collect_account发送2^256-1个token
        self.batch_transfer_from(test_account_1, test_account_2, [collect_account], [2**256-1], config.password, [0])
        # 7.1-1.4
        print("start token_test 7.1-1.4")
        # 由账户test_account_2向collect_account发送2个token
        self.batch_transfer_from(test_account_1, test_account_2, [collect_account], [2*config.magnitude], config.password, [2*config.magnitude])
        # 7.1-1.5
        print("start token_test 7.1-1.5")
        self.balance_of(test_account_2, 8*config.magnitude)
        # 由账户test_account_2向collect_account发送所有token
        self.batch_transfer_from(test_account_1, test_account_2, [collect_account], [8*config.magnitude], config.password, [8*config.magnitude])
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
        # 由账户owner向账户test_account_2发送110个token
        self.batch_transfer(sts.SIBBAY_SHT_OWNER, [test_account_2], [110*config.magnitude], sts.SIBBAY_SHT_PASSWORD, [110*config.magnitude])
        # 设置代理额度为110
        self.approve(test_account_2, test_account_1, 110*config.magnitude, config.password, 110*config.magnitude)
        # 赎回10个token
        self.batch_transfer_from(test_account_1, test_account_2, [fund_account], [10*config.magnitude], config.password, [0])
        # 打开赎回开关，并分别赎回0个，10个，100个token
        self.open_buy_sell(sts.SIBBAY_SHT_OWNER, sts.SIBBAY_SHT_PASSWORD)
        self.batch_transfer_from(test_account_1, test_account_2, [fund_account], [0], config.password, [0])
        self.batch_transfer_from(test_account_1, test_account_2, [fund_account], [10*config.magnitude], config.password, [0])
        self.batch_transfer_from(test_account_1, test_account_2, [fund_account], [100*config.magnitude], config.password, [0])
        # 7.1-1.7
        print("start token_test 7.1-1.7")
        # 冻结账户test_account_3, 并向其转账0个token，10个token
        self.froze(sts.SIBBAY_SHT_OWNER, test_account_3, sts.SIBBAY_SHT_PASSWORD)
        self.batch_transfer_from(test_account_1, test_account_2, [test_account_3], [0], config.password, [0])
        self.batch_transfer_from(test_account_1, test_account_2, [test_account_3], [10*config.magnitude], config.password, [10*config.magnitude])
        # 7.2
        print("start token_test 7.2")
        # 设置代理额度为10
        self.approve(test_account_2, test_account_1, 10*config.magnitude, config.password, 10*config.magnitude)
        # 向账户 test_account_3, test_account_4 分别发送5个，6个token
        self.batch_transfer_from(test_account_1, test_account_2, [test_account_3, test_account_4], [5*config.magnitude, 6*config.magnitude], config.password, [0, 0])
        # 向账户 test_account_3, test_account_4 分别发送2个，3个token
        self.batch_transfer_from(test_account_1, test_account_2, [test_account_3, test_account_4], [2*config.magnitude, 3*config.magnitude], config.password, [2*config.magnitude, 3*config.magnitude])
        # 向账户 test_account_3, test_account_4 分别发送2个，3个token
        self.batch_transfer_from(test_account_1, test_account_2, [test_account_3, test_account_4], [2*config.magnitude, 3*config.magnitude], config.password, [2*config.magnitude, 3*config.magnitude])

if __name__ == '__main__':
    unittest.main()
