  
# 建立私链  
1. 创建私链路径  
# su - eth  
$ mkdir privateChain  
$ cd privateChain  
  
2. 建立创世快文件文件 genesis.json, 保存以下文档内容  
{    
    "nonce": "0x0000000000000042",  
    "timestamp": "0x00",  
    "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",  
    "extraData": "0x00",  
    "gasLimit": "0xffffffff",  
    "difficulty": "0x40",  
    "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",  
    "coinbase": "0x0000000000000000000000000000000000000000",  
    "alloc": {},  
    "config": {  
        "chainId": 666,  
        "homesteadBlock": 0,  
        "eip155Block": 0,  
        "eip158Block": 0  
    }  
}  
  
  
说明:  
difficulty: 挖矿难度，值越小，挖矿速度越快  
chainId: 设置一个大于3的任意值  
  
3. 生成创世区块  
$ geth --datadir /home/eth/privateChain/chain init mygenesis.json 2>> test.log   
  
说明:  
--datadir 路径可以是相对路径  
  
4. 启动私链  
$ geth --targetgaslimit 7000000 --gasprice 0 --rpc --rpcaddr "0.0.0.0" --rpcport "8090" --rpcapi "db,eth,net,web3" --rpccorsdomain "*" --networkid 666  --datadir /home/eth/privateChain/chain console  2>>test.log  
  
说明：  
--gasprice 挖矿接收的最低gas价格，0表示所有交易都接受  
--networkid 网络id，大于3的任意值，例如当天的日期 20180819  
  
5. 启动后会进入geth命令端  
> personal.newAccount("123456")         <<< 创建账户，其中"123456"是密码  
> miner.start()                         <<< 启动挖矿，可以带参数，比如 miner.start(2)指定2个线程挖矿  
> miner.stop()                          <<< 停止挖矿  
