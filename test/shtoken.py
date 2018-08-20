
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
import settings

from config import *

class SHToken(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 初始化数据 sht-class, w3, sht
        sc = SHTClass(
            settings.SIBBAY_SHT_ADDRESS,
            settings.SIBBAY_SHT_ABI,
        )
        cls.w3 = sc.connect_to_node(settings.SIBBAY_SHT_NODE_IPC, 5)
        cls.sht = cls.w3.eth.contract(address=Web3.toChecksumAddress(settings.SIBBAY_SHT_ADDRESS), abi=settings.SIBBAY_SHT_ABI)

    # 等待确认
    def wait_tx_confirm(self, tx_hash):
        while True:
            sleep(waitting_time)
            logs = self.w3.eth.getTransactionReceipt(tx_hash)
            if logs is None:
                continue
            break
        return logs

    # 发送ether
    def send_ether(self, _from, _to, _value, _pwd):
        _from = Web3.toChecksumAddress(_from)
        _to = Web3.toChecksumAddress(_to)
        # 记录账户_to余额
        balance_old = self.w3.eth.getBalance(_to)

        # 解锁_from账户，并转账
        self.w3.personal.unlockAccount(_from, _pwd)
        tx_hash = self.w3.eth.sendTransaction({"from": _from, "to": _to, "value": _value, "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        # 查看账户_to余额
        balance_new = self.w3.eth.getBalance(_to)
        self.assertEqual(balance_new - balance_old, _value)

    # 发送token
    # _from 发送方
    # _to 接收方
    # _value token的数量
    # _pwd _from的解锁密码
    # _expect 账户_to token的变化值
    def transfer(self, _from, _to, _value, _pwd, _expect):
        _from = Web3.toChecksumAddress(_from)
        _to = Web3.toChecksumAddress(_to)
        # 记录账户_to的余额
        balance_old = self.sht.functions.balanceOf(_to).call()

        # 解锁_from账户，并发送_vaue个token给账户_to
        self.w3.personal.unlockAccount(_from, _pwd)
        tx_hash = self.sht.functions.transfer(_to, _value).transact({"from": _from, "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        # 查看账户_to的余额
        balance_new = self.sht.functions.balanceOf(_to).call()

        self.assertEqual(balance_new - balance_old, _expect);

    def transfer_from(self, _spender, _from, _to, _value, _pwd, _expect):
        _spender = Web3.toChecksumAddress(_spender)
        _from = Web3.toChecksumAddress(_from)
        _to = Web3.toChecksumAddress(_to)
        # 记录账户_to的余额
        balance_old = self.sht.functions.balanceOf(_to).call()

        # 解锁_spender账户，并发送_vaue个token给账户_to
        self.w3.personal.unlockAccount(_spender, _pwd)
        tx_hash = self.sht.functions.transferFrom(_from, _to, _value).transact({"from": _spender, "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        # 查看账户_to的余额
        balance_new = self.sht.functions.balanceOf(_to).call()

        self.assertEqual(balance_new - balance_old, _expect);

    def approve(self, _owner, _spender, _value, _pwd, _expect):
        # 转换地址
        _owner = Web3.toChecksumAddress(_owner)
        _spender = Web3.toChecksumAddress(_spender)
        # 查询代理余额
        ret = self.sht.functions.allowance(_owner, _spender).call()
        if ret == _value:
            return

        # 解锁_owner账户，并设置代理余额
        self.w3.personal.unlockAccount(_owner, _pwd)
        tx_hash = self.sht.functions.approve(_spender, _value).transact({"from": _owner, "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        # 查询代理余额
        ret = self.sht.functions.allowance(_owner, _spender).call()
        self.assertEqual(ret, _value)

    def increase_approval(self, _owner, _spender, _value, _pwd, _expect):
        # 记录代理余额
        balance_old = self.sht.functions.allowance(_owner, _spender).call()

        # 解锁_owner账户，并设置代理余额
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_owner), _pwd)
        tx_hash = self.sht.functions.increaseApproval(Web3.toChecksumAddress(_spender), _value).transact({"from": Web3.toChecksumAddress(_owner), "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        # 查询代理余额
        balance_new = self.sht.functions.allowance(_owner, _spender).call()
        self.assertEqual(balance_new - balance_old, _value)

    def decrease_approval(self, _owner, _spender, _value, _pwd, _expect):
        # 记录代理余额
        balance_old = self.sht.functions.allowance(_owner, _spender).call()

        # 解锁_owner账户，并设置代理余额
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_owner), _pwd)
        tx_hash = self.sht.functions.decreaseApproval(Web3.toChecksumAddress(_spender), _value).transact({"from": Web3.toChecksumAddress(_owner), "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        # 查询代理余额
        balance_new = self.sht.functions.allowance(_owner, _spender).call()
        self.assertEqual(balance_old - balance_new, _value)

    def batch_transfer(self, _from, _receivers, _values, _expects):
        # 转换地址，并记录余额
        for i in range(len(_receivers)):
            _receivers[i] = Web3.toChecksumAddress(_receivers[i])
            balances_old[i] = self.sht.functions.balanceOf(_receivers[i]).call()

        # 解锁_from账户，并批量发送
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_from), _pwd)
        tx_hash = self.sht.functions.batchTransfer(_receivers, _values).call({"from": Web3.toChecksumAddress(_owner), "gas": gas, "gasPrice": gas_price})

        # 查询余额，并验证
        for i in range(len(_receivers)):
            balances_new[i] = self.sht.functions.balanceOf(_receivers[i]).call()
            self.assertEqual(balances_new[i] - balances_old[i], _expects[i])

    def batch_transfer_from(self, _spender, _from, _receivers, _values, _expects):
        # 转换地址，并记录余额
        for i in range(len(_receivers)):
            _receivers[i] = Web3.toChecksumAddress(_receivers[i])
            balances_old[i] = self.sht.functions.balanceOf(_receivers[i]).call()

        # 解锁_from账户，并批量发送
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_spender), _pwd)
        tx_hash = self.sht.functions.batchTransferFrom(Web3.toChecksumAddress(_from), _receivers, _values).call({"from": Web3.toChecksumAddress(_spender), "gas": gas, "gasPrice": gas_price})

        # 查询余额，并验证
        for i in range(len(_receivers)):
            balances_new[i] = self.sht.functions.balanceOf(_receivers[i]).call()
            self.assertEqual(balances_new[i] - balances_old[i], _expects[i])

    def transfer_by_date(self, _from, _to, _values, _dates, _expect):
        # 记录余额
        balance_old = self.sht.functions.balanceOf(Web3.toChecksumAddress(_to)).call()

        # 解锁_from账户，并批量发送
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_from), _pwd)
        tx_hash = self.sht.functions.transferByDate(Web3.toChecksumAddress(_to), _values, _dates).call({"from": Web3.toChecksumAddress(_from), "gas": gas, "gasPrice": gas_price})

        # 查询余额，并验证
        balance_new = self.sht.functions.balanceOf(Web3.toChecksumAddress(_to)).call()
        self.assertEqual(balance_new - balance_old, _expect)

    def transfer_from_by_date(self, _spender, _from, _to, _values, _dates, _expect):
        # 记录余额
        balance_old = self.sht.functions.balanceOf(Web3.toChecksumAddress(_to)).call()

        # 解锁_from账户，并批量发送
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_spender), _pwd)
        tx_hash = self.sht.functions.transferByDate(Web3.toChecksumAddress(_from), Web3.toChecksumAddress(_to), _values, _dates).call({"from": Web3.toChecksumAddress(_spender), "gas": gas, "gasPrice": gas_price})

        # 查询余额，并验证
        balance_new = self.sht.functions.balanceOf(Web3.toChecksumAddress(_to)).call()
        self.assertEqual(balance_new - balance_old, _expect)

    def set_fund_account(self):
        # 查看fund account
        ret = self.sht.functions.fundAccount().call()
        if ret == Web3.toChecksumAddress(fund_account):
            return

        # 解锁owner账户，并设置fund account
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), settings.SIBBAY_SHT_PASSWORD)
        tx_hash = self.sht.functions.setFundAccount(Web3.toChecksumAddress(fund_account)).transact({"from": Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        # 验证fund account
        ret = self.sht.functions.fundAccount().call()
        self.assertEqual(ret, Web3.toChecksumAddress(fund_account))

    # 清空账户余额
    # _who 将要清空的账户
    def clear_all_sht(self, _who):
        # 获取账户余额
        balance = self.sht.functions.balanceOf(Web3.toChecksumAddress(_who)).call()

        # 将所有余额转账到回收账户
        if balance > 0:
            self.transfer(_who, collect_account, balance, password, balance)

    # 冻结账户
    # _admin 管理员
    # _who 被冻结账户
    # _pwd 管理员解锁密码
    def froze(self, _admin, _who, _pwd):
        # 查看状态
        ret = self.sht.functions.frozenList(Web3.toChecksumAddress(_who)).call()
        if ret == True:
            return

        # 解锁_admin账户并冻结账户
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_admin), _pwd)
        tx_hash = self.sht.functions.froze(Web3.toChecksumAddress(_who)).transact({"from": Web3.toChecksumAddress(_admin), "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        ret = self.sht.functions.frozenList(Web3.toChecksumAddress(_who)).call()
        self.assertEqual(ret, True)

    # 解除冻结账户
    # _admin 管理员
    # _who 被解除冻结账户
    # _pwd 管理员解锁密码
    def unfroze(self, _admin, _who, _pwd):
        # 查看状态
        ret = self.sht.functions.frozenList(Web3.toChecksumAddress(_who)).call()
        if ret == False:
            return

        # 解锁_admin账户并解冻账户
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_admin), _pwd)
        tx_hash = self.sht.functions.unfroze(Web3.toChecksumAddress(_who)).transact({"from": Web3.toChecksumAddress(_admin), "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        ret = self.sht.functions.frozenList(Web3.toChecksumAddress(_who)).call()
        self.assertEqual(ret, False)

    def set_sell_price(self, _admin, _price, _pwd):
        # 查看sell price
        ret = self.sht.functions.sellPrice().call()
        if ret == _price:
            return

        # 结算_admin账户并设置价格
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_admin), _pwd)
        tx_hash = self.sht.functions.setSellPrice(_price).transact({"from": Web3.toChecksumAddress(_admin), "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        ret = self.sht.functions.sellPrice().call()
        self.assertEqual(ret, _price)

    def set_buy_price(self, _admin, _price, _pwd):
        # 查看sell price
        ret = self.sht.functions.buyPrice().call()
        if ret == _price:
            return
        # 结算_admin账户并设置价格
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(_admin), _pwd)
        tx_hash = self.sht.functions.setBuyPrice(_price).transact({"from": Web3.toChecksumAddress(_admin), "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        ret = self.sht.functions.buyPrice().call()
        self.assertEqual(ret, _price)

    def open_buy_sell(self):
        # 查看状态
        ret = self.sht.functions.buySellFlag().call()
        if ret == True:
            return

        # 解锁owner账户，并打开购买和赎回开关
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), settings.SIBBAY_SHT_PASSWORD)
        tx_hash = self.sht.functions.openBuySell().transact({"from": Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        ret = self.sht.functions.buySellFlag().call()
        self.assertEqual(ret, True)

    def close_buy_sell(self):
        # 查看状态
        ret = self.sht.functions.buySellFlag().call()
        if ret == False:
            return

        # 解锁owner账户，并打开购买和赎回开关
        self.w3.personal.unlockAccount(Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), settings.SIBBAY_SHT_PASSWORD)
        tx_hash = self.sht.functions.closeBuySell().transact({"from": Web3.toChecksumAddress(settings.SIBBAY_SHT_OWNER), "gas": gas, "gasPrice": gas_price})

        # 等待确认
        self.wait_tx_confirm(tx_hash)

        ret = self.sht.functions.buySellFlag().call()
        self.assertEqual(ret, False)

