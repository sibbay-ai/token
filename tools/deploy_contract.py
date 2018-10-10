
from ether_node import EtherNode
import config as cfg

if __name__ == "__main__":
    # get ether node
    enode = EtherNode()
    # decrype keystore file
    acc = enode.decrypt_keystore(cfg.ETH_KEYSTORE_FILE, None)
    # deploy contract
    address,abi = enode.create_contract(acc, cfg.ETH_CONTRACT_SHT_FILE, True)
    print("contract address:", address)
