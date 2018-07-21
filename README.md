# token

## SHT Server
SHT server is a tokening watching server based on python3, which will watch all token's transfer events that are transfered to owner and pay ether to transaction's sender.
### configuration: setting.py
* price: ether price and decimals, sht price and decimals
> SIBBAY_SHT_ETHER_PRICE = env("SIBBAY_ETHER_PRICE", 0.0)
> SIBBAY_SHT_ETHER_DECIMALS = env("SIBBAY_DECIMALS", 18)
> SIBBAY_SHT_SHT_PRICE = env("SIBBAY_SHT_PRICE", 0.01)
> SIBBAY_SHT_SHT_DECIMALS = env("SIBBAY_DECIMALS", 0)

* node path, should config the ipc' fullpath of your ethereum node
> SIBBAY_SHT_NODE_IPC  = env("SIBBAY_NODE_IPC", "/home/eth/ethereumTest/chain/geth.ipc")

* sht owner and password, which will send ether to whom selling token
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
4. how to update SHT price
> python update_sht_price.py

### mongodb
all data are storged in database sht of mongoDB,
collection col_token_transfer stores all token transfer event
collection col_token_sell stores all sell event which means transfer token to owner(SIBBAY_SHT_OWNER)
collection col_token_price stores token price and ether prices information

### update token price
1. modify token price SIBBAY_SHT_SHT_PRICE
2. execute: python update_sht_price.py

### unittest
unit test needs correct ethereum node info and mongodb info, so please configure all info in settings.py
> cd test
> python event_test.py
