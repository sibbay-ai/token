from web3 import Web3
from time import sleep
import json

import config as cfg
import getpass


class EtherNode():
    def __init__(self):
        # nonce flag and value
        self.nonce_value = {}
        #  connect to node
        while True:
            self.w3 = Web3(Web3.HTTPProvider(cfg.ETH_NODE_HTTP, {"timeout": 30}))
            if self.w3.isConnected() == False:
                print("node is not connected, wait " + str(5) + " second")
                sleep(5)
            else:
                print("connect to node by http: " + cfg.ETH_NODE_HTTP)
                break

    # wait confirmed
    def wait_tx_confirm(self, tx_hash):
        while True:
            sleep(cfg.ETH_WAIT_INTERNAL)
            logs = self.w3.eth.getTransactionReceipt(tx_hash)
            if logs is None:
                continue
            break
        return logs

    # decrypt keystore file
    # return accout obj: {address, privateKey, signTransaction, encrypt, signHash}
    def decrypt_keystore(self, _kf, _pwd):
        if _pwd is None:
            _pwd = getpass.getpass("password:")
        # open keystore file
        with open(_kf, 'r') as fp:
            # load json file
            fj = json.load(fp)
            # decrypt
            private_key = self.w3.eth.account.decrypt(fj, _pwd)
            return self.w3.eth.account.privateKeyToAccount(private_key)
        return None

    # get nonce
    def get_nonce(self, address):
        # get nonce from dict
        nonce = self.nonce_value.get(address)
        if nonce is None:
            # get nonce from node
            nonce = self.w3.eth.getTransactionCount(address);

        #update nonce
        self.nonce_value[address] = nonce + 1
        return nonce

    # create contract
    # return: address, abi
    def create_contract(self, acc_owner, build_file, wait=False):
        with open(build_file, 'r') as fp:
            # load json file
            fj = json.load(fp)
            # get bytecode, deployedBytecode, abi
            bc = fj['bytecode']
            dbc = fj["deployedBytecode"]
            abi = fj["abi"]
            # get contract
            shtc = self.w3.eth.contract(abi=abi, bytecode=bc, bytecode_runtime=dbc)
            # build transaction
            shtx = shtc.constructor(self.w3.toChecksumAddress(cfg.OWNER_ACCOUNT), self.w3.toChecksumAddress(cfg.FUND_ACCOUNT)).buildTransaction({
                "from": acc_owner.address,
                "gas": cfg.ETH_TX_GAS,
                "gasPrice": cfg.ETH_TX_GAS_PRICE,
                "nonce": self.get_nonce(acc_owner.address)
                })
            # sign transaction
            raw_tx = acc_owner.signTransaction(shtx)
            # send raw transaction
            tx_hash = self.w3.eth.sendRawTransaction(raw_tx["rawTransaction"])
            print("tx hash:", str(self.w3.toHex(tx_hash)))
            # wait tx confirmed
            if wait is True:
                ret = self.wait_tx_confirm(tx_hash)
                print("deploy contract", build_file, "successed, gas used:", ret["gasUsed"])
                return ret["contractAddress"], fj["abi"]
        return None,fj["abi"]

