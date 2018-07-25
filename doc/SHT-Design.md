
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
1. function totalSupply() public view returns (uint256);
总供应量: 1,000,000,000,--------待确认
返回值：token总量
2. function balanceOf(address who) public view returns (uint256);
查询账户余额
参数 who: 查询的账户
返回值: 账户who的余额
3. function transfer(address to, uint256 value) public returns (bool);
token转账:
    包含所有普通转账 -- 所有用户权限
    包含回收token, 即发送给合约本身或者owner的转账, -- 可卖出账户权限
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
暂停合约，暂停所有账户token交易, 仍可以执行查询操作 -- administrator权限
4. function unpause() public;
取消暂停，恢复所有账户token交易 -- administrator权限
5. function froze(address who) public;
冻结账户，冻结指定账户token交易，仍可以执行查询操作 -- administrator权限
参数 who: 指定的冻结账户
6. function unfroze(address who) public;
取消冻结，恢复指定账户token交易 -- administrator权限
参数 who: 指定的取消冻结账户
7. function addAdministrator(address admin) public;
增加管理账户 -- owner 权限
参数 admin: 指定的管理者
8. function delAdminnistrator(address admin) public;
取消管理账户 -- owner 权限
参数 admin: 取消的管理者
9. function batchTransfer(address receivers[], uint256 vlaue) pubic;
批量转发 -- administrator权限
参数 receivers: token的接收账户
     value: token的转账数量


#### option events
1. event Pause();
暂停事件
2. event Unpause();
取消暂停事件
3. event Froze(address indexed who);
冻结事件
参数 who: 指定的冻结账户
4. event Unfroze(address indexed who);
取消冻结事件
参数 who: 指定的取消冻结账户
5. event AddAdministrator(address indexed owner, address indexed admin);
增加管理账户
参数 owner: 增加管理账户的操作者
     admin: 增加的管理账户
6. event DelAdministrator(address indexed owner, address indexed admin);
取消管理账户
参数 owner: 取消管理账户的操作者
     admin: 取消的管理账户

### buy/sell token
#### interface
1. function buy() public;
买入token
2. function sell(uint256 value) public;
卖出token，即卖给合约或合约管理者 -- 可卖出账户权限, 即只有可卖出账户可以卖出
参数 value: token的卖出数量
3. function setPrice(uint256 price) public;
设置价格，即token的以太币价格, 即一个token的以太币价格
参数 price:  指定的token的价格, 以太坊单位 wei
4. addSeller(address seller) public;
添加可卖出账户 -- administrator 权限
参数 seller: 指定的可卖出账户
5. delSeller(address seller) public:
取消可卖出账户 -- administrator 权限
参数 seller: 取消的课卖出账户

#### events
1. event Buy(address indexed who, uint256 value);
买入事件
参数 who: token买入账户
     value: token买入数量
2. event Sell(address indexed who, uint256 value);
卖出事件
参数 who: token卖出账户
     value: token卖出数量
3. event SetPrice(uint256 price);
设置汇率事件
参数 price:  当期token的价格
4. event AddSeller(address indexed admin, address indexed seller);
添加可卖出账户事件
参数 admin: 执行该操作的管理者
参数 seller: 指定的可卖出账户
4. event DelSeller(address indexed admin, address indexed seller);
取消可卖出账户事件
参数 admin: 执行该操作的管理者
参数 seller: 取消的可卖出账户


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
