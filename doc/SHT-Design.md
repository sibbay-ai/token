  
# SHT-Design  
  
## requirements  
  
1. 账户余额查询到的是总余额，包括可用余额和锁定期的余额.  
2. 锁定期的到期时间必定是某个月第一天0点0分0秒.  
3. transferByDate 为向某用户转入一定量带有锁定期的token.  
    如果锁定期的到期时间小于当前时间，则为普通转账，直接将余额发送给指定账户  
4. 账户余额实现方式 mapping  
   账户锁定期余额实现方式 mapping(时间 => 余额)  
   实现查询总余额，可用余额，锁定期及其对应余额列表  
5. transfer 为ERC20标准转账操作  
    该操作实现可回收token的功能，即向指定的特殊用户发送token，则合约自动回传对应价值的以太币  
    该操作对sender进行类型判断，如果其带有锁定期的token，且锁定期到期，则将锁定期token放入可用余额  
6. 实现简单的buy功能，即可以通过buy接口购买token,  
   购买token的价格应该高于自动赎回的价格  

7. 增加新接口：可以取回合约的所有以太币给Owner
  
## contract  
### ERC20 standard  
### all ERC20 attributions  
1. name  
Token名字: Sibbay Health Token  
2. symbol  
Token 符号: SHT  
3. decimals  
小数点位数: 18  
  
#### all ERC20 interfaces  
1. function totalSupply() public view returns (uint256);  
总供应量: 1,000,000,000 即 10个亿  
返回值：token总量  
2. function balanceOf(address who) public view returns (uint256);  
查询账户余额  
参数 who: 查询的账户  
返回值: 账户who的余额  
3. function transfer(address to, uint256 value) public returns (bool);  
token转账:  
    包含所有普通转账 -- 所有用户权限  
    包含回收token, 即发送给合约本身或者owner的转账, -- 所有账户都有赎回权限  
参数 to: token接收账户  
     value: token转账数量  
返回值： 成功返回true  
4. function allowance(address owner, address spender) public view returns (uint256);  
查询代理余额  
参数 owner: token拥有者, 即被代理人  
     spender: token使用者，即代理人  
返回值： token的代理数量  
5. function transferFrom(address from, address to, uint256 value)  public returns (bool);  
token转账，转账被代理人账户  
参数 from: 被代理人  
     to: token接收账户  
     value: token转账数量  
返回值： 成功返回True  
6. function approve(address spender, uint256 value) public returns (bool);  
指定代理  
参数 spender: 代理人  
     value: token代理数量  
返回值：成功返回true  
  
#### all ERC20 events  
1. event Transfer(address indexed from, address indexed to, uint256 value);  
转账事件  
参数 from: token发送账户  
     to: token接受账户  
     value: token转账数量  
2. event Approval(address indexed owner, address indexed spender, uint256 value);  
代理事件  
参数 owner: 被代理人  
     spender: 代理人  
     value: token转账数量  
3 event TransferFrom(address indexed spender, address indexed from, address indexed to, uint256 value);  
代理转账事件  
参数 spender: 代理人  
     from: 被代理人  
     to: token接收账户  
     value: token转账数量  
  
#### option interfaces  
1. function increaseApproval(address spender, uint addedValue) public returns (bool);  
提高代理额度  
参数 spender: 代理人  
     addedValue: 增加的token代理数量  
返回值：成功返回true  
2. function decreaseApproval(address spender, uint subtractedValue) public returns (bool);  
降低代理额度  
参数: spender: 代理人  
      subtractedValue: 降低的token代理数量  
返回值： 成功返回true  
3. function pause() public;  
暂停合约，暂停所有账户token交易, 仍可以执行查询操作 -- owner 权限  
4. function unpause() public;  
取消暂停，恢复所有账户token交易 -- owner权限  
5. function froze(address who) public;  
冻结账户，冻结指定账户token交易，仍可以执行查询操作 -- administrator权限  
参数 who: 指定的冻结账户  
6. function unfroze(address who) public;  
取消冻结，恢复指定账户token交易 -- administrator权限  
参数 who: 指定的取消冻结账户  
7. function addAdministrator(address admin) public;  
增加管理账户 -- owner 权限  
参数 admin: 指定的管理者  
8. function delAdministrator(address admin) public;  
取消管理账户 -- owner 权限  
参数 admin: 取消的管理者  
9. function batchTransfer(address[] receivers, uint256[] value) pubic;  
批量转发 -- administrator权限  
参数 receivers: token的接收账户  
     value[]: token的转账数量, 与receivers 一一对应  
  
  
#### option events  
1. event Pause();  
暂停事件  
2. event Unpause();  
取消暂停事件  
3. event Froze(address indexed admin, address indexed who);  
冻结事件  
参数 who: 指定的冻结账户  
4. event Unfroze(address indexed admin, address indexed who);  
取消冻结事件  
参数 who: 指定的取消冻结账户  
5. event AddAdministrator(address indexed admin);  
增加管理账户  
参数 admin: 增加的管理账户  
6. event DelAdministrator(address indexed admin);  
取消管理账户  
参数 admin: 取消的管理账户  
  
### buy/sell token  
#### interface  
1. function buy() public;  
买入token, 实现简单的token买入功能, 买入价格应高于卖出价格，即赎回价格  
2. function sell(uint256 value) public;  
卖出token，即赎回token，将token转入指定的特殊账户，并回传对应数量的以太币  
参数 value: token的卖出数量  
3. function setSellPrice(uint256 price) public;  
设置卖出价格，即token的赎回以太币价格, 即一个token的以太币价格 -- administrator 权限  
参数 price:  指定的token卖出的价格, 以太坊单位 wei  
4. function setBuyPrice(uint256 price) public;  
设置买入价格，即token的买入以太币价格，即一个token的以太币价格 -- administrator 权限  
参数 price: 指定的token买入价格, 以太坊单位 wei  
5. function setFundAccount(address fund) public;  -- owner 权限  
设置特殊资金账户，用以接收购买token的以太币和赎回的token  
参数 fund: 特殊账户的地址  
  
#### events  
1. event Buy(address indexed who, uint256 value);  
买入事件  
参数 who: token买入账户  
     value: token买入数量  
2. event Sell(address indexed who, uint256 value);  
卖出事件  
参数 who: token卖出账户  
     value: token卖出数量  
3. event SetSellPrice(uint256 price);  
设置卖出价格事件，即token的赎回价格  
参数 price:  token的卖出价格  
4.event SetBuyPrice(uint256 price);  
设置买入价格事件，即token的购买价格  
参数 price: token的购买价格  
5. event SetFundAccount(address indexed fund);  
设置设置特殊账户事件  
参数: fund 特殊账户地址  
  
  
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
