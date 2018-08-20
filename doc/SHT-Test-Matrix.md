
# 测试点矩阵法

## 测试点
1. 账户维度
    -- 普通账户
    -- 代理账户
    -- 冻结账户
    -- 管理账户
    -- owner账户

2. 接口维度
    -- transfer
    -- transferFrom
    -- batchTransfer
    -- batchTransferFrom
    -- transferByDate
    -- transferFromByDate
    -- approve
    -- increaseApproval
    -- decreaseApproval
    -- buy
    -- sell
    -- setSellPrice
    -- setBuyPrice
    -- setFundAccount
    -- openBuySell
    -- closeBuySell
    -- pause
    -- unpause
    -- froze
    -- unfroze
    -- addAdministrator
    -- delAdministrator
    -- withdraw

3. 状态维度
    -- 合约暂停
    -- 合约未暂停
    -- 购买和赎回功能打开
    -- 购买和赎回功能关闭

4. 行为维度
    -- 向0地址转账
    -- 向非0地址转账
    -- 向赎回地址转账
    -- 向非赎回地址转账

5. 参数维度
    -- 无锁定期余额
    -- 有锁定期余额,但无到期锁定期
    -- 有锁定期余额,部分锁定期到期
    -- 有锁定期余额,全部锁定期到期
    -- token余额足够
    -- token余额不够
    -- 合约预存ether足够
    -- 合约预存ether不够
    -- fundAccount预存token足够
    -- fundAccount预存token不够
    -- 转账0个token
    -- 转账大于0个token
    -- 代理余额足够
    -- 代理余额不够
    -- 批量转账 receivers 和 vlaues 长度相等
    -- 批量转账 receivers 和 vlaues 长度不等
    -- 分期转账 values 和 dates 长度相等
    -- 分期转账 values 和 dates 长度不等
    -- 分期转账 锁定期小于当前日期
    -- 分期转账 锁定期大于当前日期，接收账户没有锁定期token
    -- 分期转账 锁定期大于当前日期，接收账户有锁定期token, 锁定期小于接受账户原最小锁定期
    -- 分期转账 锁定期大于当前日期，接收账户有锁定期token, 锁定期大于接受账户原最大锁定期
    -- 分期转账 锁定期大于当前日期，接收账户有锁定期token, 锁定期等于接收账户的某个锁定期
    -- 分期转账 锁定期大于当前日期，接收账户有锁定期token, 锁定期在接收账户的最大和最小锁定期之间
    -- ehter余额不够
    -- ehter余额足够
    -- 购买token，发送ether为0
    -- 购买token，发送ether大0
    -- 赎回价格默认值0
    -- 购买价格默认值0
    -- 基金账户默认值0
    -- 设置赎回价格 设置赎回价格等于0
    -- 设置赎回价格 设置赎回价格大于0
    -- 设置购买价格 设置赎回价格等于0
    -- 设置购买价格 设置赎回价格大于0
    -- 设置基金账户 设置为0地址0
    -- 设置基金账户 设置为非0地址


