# token

## SHT token
### How to deploy
1. need install npm, truffle
> yum install npm
> npm install -g truffle

2. use truffle to deploy your contract
> mkdir sht                       <<<< 建立一个目录用来创建工程
> cd sht
> truffle init                    <<<< 初始化工程
copy all contract files into directory contracts.  
copy all migration files into directory migrations.  
copy truffle.js to overwrite the file truffle.js.  
> truffle compile                 <<<< 编译文件， 在sht目录下
> truffle migrate --network roptest <<<< 部署合约

note: 部署的之前，需要对用来部署的账号进行解锁。即在节点 personal.unlock操作。  
      由于网络环境或者gasprice的影响，部署时间可能会很慢，这个时候，需要在部署过程中多次解锁。防止解锁超时导致合约部署失败。  

3. truffle.js
部署配置文件，这里面可以配置部署所需要的参数, 下面介绍网络配置  
  networks: {  
      roptest: {                            <<<< 网路的名字，上面部署的时候指定 --network roptest  
          host: "localhost",                <<<< 节点rpc的地址，这里默认是当前主机, 与节点启动脚本对应, 即start.sh中 --rpcaddr  
          port: 7454,                       <<<< 节点rpc的端口, 与节点启动脚本对应，即start.sh中 --rpcport  
          network_id: "3",                  <<<< 网络id，这里用测试节点 ropsten 的网络id，即3. 主网是 1.  
          gas: 6000000,                     <<<< 允许最大消耗的gas, 这里是6000000   
          gasPrice: 4000000000,             <<<< gas 价格， 4 wei  
          from: "0x6d31f4bedce01850e4268778d1596798c5075f71"   <<<< 设置由哪个账户部署，这个根据节点所需更改  
      },  
      main: {   <<<< 公网先注释掉，防止误操作
          //host: "localhost",  
          //port: 7454,  
          //network_id: "1",  
          //gas: 6000000,  
          //gasPrice: 4000000000,  
          //from: "0x6d31f4bedce01850e4268778d1596798c5075f71"  
      }  
  }  


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

### How to exit
> kill -10 <process-id>

### unittest
unit test needs correct ethereum node info and mongodb info, so please configure all info in settings.py
> cd test
> python event_test.py
