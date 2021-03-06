# SHT-逻辑设计文档

## 简介

## 功能要求
### ERC20功能
1. token 名字，符号，小数位数
2. 查询总供应量
3. 查询余额
4. 转账
5. 授权代理
6. 查询授权代理额度
7. 代理转账

### 扩展管理功能
1. 暂停/取消暂停合约
2. 冻结/取消冻结账户
3. 添加/删除管理员
4. owner超级管理员

### 扩展普通功能
1. 转账， 对普通转账功能的扩展
    - 赎回功能，向指定用户转账，可以返回对应价格的ether 
    - 处罚功能，对于冻结用户，可以向0地址转账
    - 获取到期的锁定期余额
2. 批量转账
    - 向多个地址转账不同的额度
3. 代理批量转账
    - 授权的代理可以向多个地址转账不同的额度
4. 锁定期转账
    - 转账有多个锁定期的不同金额，只有到期之后，才可以使用，没到期则不能使用
5. 代理锁定期转账
    - 授权的代理可以转账有多个锁定期的不同金额，只有到期之后，才可以使用，没到期则不能使用
6. 查询余额
    - 查询余额是总余额，包括可用余额和锁定期的余额
7. 购买
    - 通过buy接口，购买一定量的token
8. 赎回
    - 通过sell接口，赎回一定的token，同转账功能的赎回功能
9. 设置购买价格
    - 设置token的购买价格
10. 设置赎回价格
    - 设置token的赎回价格
11. 设置赎回地址
    - 设置赎回地址，只有在打开赎回功能的时候，才可以向赎回地址转账
12. 开放/关闭购买赎回功能
    - 开发购买赎回功能
    - 关闭购买赎回功能

### 交易所问题确认
1. 向赎回地址转账会回传一定的以太币
2. 查询到的余额，包括锁定期余额，如果有未到期的余额会导致转账失败，即使转账额度小于总余额
3. 冻结用户可以向0地址转账, 而普通用户不能
4. 代理转账不能向赎回地址转账

## ERC20接口

## 扩展接口
