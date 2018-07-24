
# SHT-Design

## contract
### ERC20 standard
### all ERC20 attributions
1. name
Token名字: Sibbay Health Token
2. symbol
Token 符号: SHT
3. decimals
小数点位数: 10

#### all ERC20 interfaces
1. totalSupply
总供应量:    --------待确认
2. balanceOf
查询账户余额
3. transfer
token转发
4. allowance
查询代理余额
5. transferFrom
token转发，转发被代理人账户
6. approve
指定代理

#### all ERC20 events
1. Transfer
转发事件
2. Approval
代理事件

#### option interfaces
1. increaseApproval
提高代理额度
2. decreaseApproval
降低代理额度
3. increSupply
增发token  -- owner权限，即只有管理员才能操作
4. burn
销毁token
5. kill -- need to confirm !!!
销毁合约 ---需要确认是否需要
6. pause
暂停合约，暂停所有账户token交易, 仍可以执行查询操作 -- owner权限
7. unpause
取消暂停，恢复所有账户token交易 -- owner权限
8. froze
冻结账户，冻结指定账户token交易，仍可以执行查询操作 -- owner权限
9. unfroze
取下冻结，恢复指定账户token交易 -- owner权限

#### option events
1. Increase
增发事件
2. Burn
销毁事件
3. Pause
暂停事件
4. Unpause
取消暂停事件
5. Froze
冻结事件
6. Unfroze
取消冻结事件

### buy/sell token
#### interface
1. buy
买入token
2. sell
卖出token，即卖给合约或合约管理者
3. setRate
设置汇率，即token的以太币价格, 即一个token的以太币价格

#### events
1. Buy
买入事件
2. Sell
卖出事件
3. SetRate
设置汇率事件

## server
### watch all transfer event
1. watch all transfer event
监控所有token交易事件
2. watch all buy/sell event
监控所有买入卖出事件

### update price
1. SHT price
可手动更新token价格, 单位 CNY
2. Ether price
可实时查询以太币价格，单位 CNY
3. set rate to contract
自动每天设置token的汇率，即1 token的以太币价格
