
# eth configuration

# ethereum node's htpp
#ETH_NODE_HTTP = "http://127.0.0.1:8090"
ETH_NODE_HTTP = "https://ropsten.infura.io/v3/99a79f80961b4db7aab7c9f54375eda7"
ETH_WAIT_INTERNAL = 5

# transaction config
# gas: 7000000, gasPrice: 1 wei, 1000000000
ETH_TX_GAS = 7000000
ETH_TX_GAS_PRICE = 8000000000

# keystore file
ETH_KEYSTORE_FILE = "/home/henry/myEtherum/chain/keystore/UTC--2018-10-19T08-53-41.743071688Z--ee21ebb177539f247d4c9cc6255facf2af21e6b4"
# owner and fund account
#OWNER_ACCOUNT = "0xee21ebb177539f247d4c9cc6255facf2af21e6b4"
#FUND_ACCOUNT = "0x28b7a7fd5e876e5e2ac50dbb66860d80b2e2db3a"
OWNER_ACCOUNT = "0x6Bd5f0f1846F913CfF230014C32aC6F4E4fAd4B0"
FUND_ACCOUNT = "0x8A0e4B86CD76684057BC0e62B5753F513fC332BB"


# builded files of contract
ETH_CONTRACT_SHT_FILE = "../build/contracts/SibbayHealthToken.json"


