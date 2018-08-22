
# 测试点矩阵法

## 测试点
1. 账户维度
    accD-1 普通账户
    accD-2 代理账户
    accD-3 冻结账户
    accD-4 管理账户
    accD-5 owner账户

2. 接口维度
    interD-1 transfer
    interD-2 transferFrom
    interD-2 batchTransfer
    interD-4 batchTransferFrom
    interD-5 transferByDate
    interD-6 transferFromByDate
    interD-7 approve
    interD-8 increaseApproval
    interD-9 decreaseApproval
    interD-10 buy
    interD-11 sell
    interD-12 setSellPrice
    interD-13 setBuyPrice
    interD-14 setFundAccount
    interD-15 openBuySell
    interD-16 closeBuySell
    interD-17 pause
    interD-18 unpause
    interD-19 froze
    interD-20 unfroze
    interD-21 addAdministrator
    interD-22 delAdministrator
    interD-23 withdraw

3. 状态维度
    3.1 合约状态
        contSD-1 合约暂停
        contSD-2 合约未暂停

    3.2 购买赎回功能状态
        buySellSD-1 购买和赎回功能打开
        buySellSD-2 购买和赎回功能关闭

4. 行为维度
    4.1 地址值是否为0
        destAddrZD-1 向0地址转账
        destAddrZD-2 向非0地址转账
    4.2 地址是否为赎回地址
        destAddrBsFD-1 向赎回地址转账
        destAddrBsFD-2 向非赎回地址转账

5. 参数维度
    5.1 锁定期余额
        lockBD-1 无锁定期余额
        lockBD-2 有锁定期余额,但无到期锁定期
        lockBD-3 有锁定期余额,部分锁定期到期
        lockBD-4 有锁定期余额,全部锁定期到期
    5.2 token余额
        tokenBD-1 token余额足够
        tokenBD-2 token余额不够
    5.3 合约ehter余额
        contBD-1 合约预存ether足够
        contBD-2 合约预存ether不够
    5.4 fundAccount token余额
        fundBD-1 fundAccount预存token足够
        fundBd-2 fundAccount预存token不够
    5.5 转账额度
        valueBD-1 转账0个token
        valueBD-2 转账大于0个token
    5.6 代理额度
        allowBD-1 代理余额足够
        allowBD-2 代理余额不够
    5.7 批量转账:
        batchTD-1 批量转账 receivers 和 vlaues 长度不等
        batchTD-2 批量转账 receivers 和 vlaues 长度相等
    5.8 分期转账
        dateTD-1 分期转账 values 和 dates 长度不等
        dateTD-2 分期转账 values 和 dates 长度相等
        dateTD-3 分期转账 锁定期小于当前日期
        dateTD-4 分期转账 锁定期大于当前日期，接收账户没有锁定期token
        dateTD-5 分期转账 锁定期大于当前日期，接收账户有锁定期token, 锁定期小于接受账户原最小锁定期
        dateTD-6 分期转账 锁定期大于当前日期，接收账户有锁定期token, 锁定期大于接受账户原最大锁定期
        dateTD-7 分期转账 锁定期大于当前日期，接收账户有锁定期token, 锁定期等于接收账户的某个锁定期
        dateTD-8 分期转账 锁定期大于当前日期，接收账户有锁定期token, 锁定期在接收账户的最大和最小锁定期之间
    5.9 sender账户ether余额
        senderBD-1 sender账户ehter余额不够
        senderBD-2 sender账户ehter余额足够
    5.10 购买token
        buyVD-1 购买token，发送ether为0
        buyVD-2 购买token，发送ether大0
    5.11 赎回价格
        sellPD-1 赎回价格默认值0
        sellPD-2 设置赎回价格 设置赎回价格等于0
        sellPD-3 设置赎回价格 设置赎回价格大于0
    5.12 购买价格
        buyPD-1 购买价格默认值0
        buyPD-2 设置购买价格 设置购买价格等于0
        buyPD-3 设置购买价格 设置购买价格大于0
    5.13 基金账户
        fundAccD-1 基金账户默认值0
        fundAccD-2 设置基金账户 设置为0地址0
        fundAccD-3 设置基金账户 设置为非0地址


