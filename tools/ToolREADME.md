
# Tool usage

## deploy_contract.py
部署合约专用脚本  
配置文件config.py  
```
# 节点rpc信息，交易等待时间默认5s
ETH_NODE_HTTP = "http://127.0.0.1:8090"
ETH_WAIT_INTERNAL = 5

# 交易花费gas上限和gas价格 设置
# 测试链上目前gas花费为5777357, 设置大于此值即可
# gas价格默认1wei
# 定稿时可接受的gas价格为 5-7 wei, 比较合理
ETH_TX_GAS = 6000000
ETH_TX_GAS_PRICE = 1000000000

# keystore文件，即部署合约用的账户私钥文件
# 解锁账户的密码会在运行脚本时候提示输入
# 运行完之后，应将该文件备份并删除，防止他人获取该文件
ETH_KEYSTORE_FILE = "/home/henry/tmp/UTC--2018-08-19T06-31-16.012953394Z--09de6b21f6c115871e6440ece7950fe26b6764fd"


# 要部署的合约编译得到的json文件
# 目前该脚本不支持部署合约传入参数
ETH_CONTRACT_SHT_FILE = "../build/contracts/SibbayHealthToken.json"


```
