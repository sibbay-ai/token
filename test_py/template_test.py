import unittest
from web3 import Web3

import settings as sts
import config
from shtoken import SHToken

accounts = config.accounts[:]


class TestTransfer(SHToken):
    def test_transfer(self):

        # base accounts and password
        # 基础账号, 供测试使用，建议预存到该账户 100个token + 100个ether
        base_acc = "0x...................."
        base_pwd = "123456"

        # 创建测试账户, accounts[1], accounts[2]
        # 创建账户并保存到accounts数组，这是其创建账户的方法，也可以另外记录保存，不比加到accounts数组
        # 其中accounts[0] 默认是 0 地址
        accounts.append(self.create_account(config.password))
        accounts.append(self.create_account(config.password))

        # 转账从账户base_acc向accounts[1]转账1个token
        # 第一个 1*magnitude 代表转账的数量
        # 第二个 1*magnitude 代表accounts[1]增加的数量
        self.transfer(base_acc, accounts[1], 1*config.magnitude, base_pwd, 1*config.magnitude)

        # 设置accounts[1]代理base_acc 10个token
        # 第一个 10*magnitude 代表代理的数量
        # 第二个 10*magnitude 代表accounts[1]代理的实际数量
        self.approve(base_acc, accounts[1], 10*config.magnitude, base_pwd, 10*config.magnitude)

        # 转账以太币
        # 从账户base_acc向accounts[1]转账1个以太币
        # 因为测试用的进行操作需要消耗gas，所以要提前转账一部分以太币给测试账户
        self.send_ether(base_acc, accounts[1], 1*config.magnitude, base_pwd)

        # 所有接口可以在 shtoken.py 中找到
        # 接口定义的原则是： 第一个参数一般为该交易的from
        #                    后面跟上接口的所有参数
        #                    最后加上from的解锁密码和期望值

        # create_account
        # send_ether
        # transfer
        # transfer_from
        # approve
        # increase_approval
        # decrease_approval
        # batch_transfer
        # batch_transfer_from
        # transfer_by_date
        # transfer_from_by_date
        # set_fund_account
        # clear_all_sht             清空账户的所有余额，可能会失败，如果有未到期的
        # clear_all_ava_sht         清空所有可用的余额
        # froze
        # unfroze
        # set_sell_price
        # set_buy_price
        # open_sell
        # close_sell
        # open_buy
        # close_buy
        # buy
        # sell
        # pause
        # unpause
        # add_administrator
        # del_administrator
        # withdraw                  取回所有合约里的以太币



if __name__ == '__main__':
#    connect(alias="sht", host=sts.SIBBAY_MONGODB_SHT_HOST)
    unittest.main()

