# token

## SHT Server
### configuration
* price: ether price and decimals, sht price and decimals
> etherPrice = 0.0
> etherDecimals = 18
> shtPrice = 0.01
> shtDecimals = 0

* log path
> shtDecimals = 0

* node path, should config the ipc' fullpath of your ethereum node
> nodePath = "/home/henry/etest/chain/geth.ipc"

* mongodb: ip and port
> mongoDB_ip = "127.0.0.1"
> mongoDB_port = 27017

* sht own, which will send ether to whom selling token
> owner = "0x6d31f4bedce01850e4268778d1596798c5075f71"

* sht contract's address and abi
> address = "0xC88c59626cBe8D56b56e824C0E1d33d79b1F1dFf"
> abi = '[........]'

### how to run
1. clone shtServer folder in the path where you want to deploy
2. modify the config as above mentioned 
3. write price config into mongodb:
> python config.py
4. start server
> nohup ./start.sh &
