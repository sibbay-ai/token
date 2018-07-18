# token

## SHT Server
### configuration: setting.py
* price: ether price and decimals, sht price and decimals
> SIBBAY_SHT_ETHER_PRICE = env("SIBBAY_ETHER_PRICE", 0.0)
> SIBBAY_SHT_ETHER_DECIMALS = env("SIBBAY_DECIMALS", 18)
> SIBBAY_SHT_SHT_PRICE = env("SIBBAY_SHT_PRICE", 0.01)
> SIBBAY_SHT_SHT_DECIMALS = env("SIBBAY_DECIMALS", 0)

* log path
> SIBBAY_SHT_LOG_PATH = env("SIBBAY_LOG_PATH", "./sht.log")

* node path, should config the ipc' fullpath of your ethereum node
> SIBBAY_SHT_NODE_IPC  = env("SIBBAY_NODE_IPC", "/home/eth/ethereumTest/chain/geth.ipc")

* mongodb: ip and port
> SIBBAY_SHT_NODE_IPC  = env("SIBBAY_NODE_IPC", "/home/eth/ethereumTest/chain/geth.ipc")

* sht own and password, which will send ether to whom selling token
> SIBBAY_SHT_OWNER = env("SIBBAY_SHT_OWNER", "0x6d31f4bedce01850e4268778d1596798c5075f71")
> SIBBAY_SHT_PASSWORD = env("SIBBAY_SHT_PASSWORD", "123456")

* sht contract's address and abi
> address = "0xC88c59626cBe8D56b56e824C0E1d33d79b1F1dFf"
> abi = '[........]'

### how to run
1. clone shtServer folder in the path where you want to deploy
2. modify the config as above mentioned
3. start server
> nohup ./start.sh &
