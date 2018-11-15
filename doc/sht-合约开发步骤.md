  
# sht 合约开发步骤  
已测试为导向的合约开发步骤  
  
1. 定义合约所有接口  
合约所有功能以接口为准, 即在调研合约需求的时候，所有需求均以接口为准则。  
  
sht token合约需求:    
> ERC20 标准  
> 账户余额分为可用余额和锁定余额, 其中锁定余额只有到锁定期到期才能使用  
> 批量转账token功能  
> 代理批量转账token功能  
> 锁定期转账功能  
> 代理锁定期转账功能  
> 管理员功能，添加/删除管理员  
> 冻结账户功能，冻结/解冻账户功能  
> 合约暂停功能，暂停/取消暂停合约功能  
> 特殊基金账户用来购买/赎回token  
> 设置token赎回价格  
> 设置token购买价格  
> 设置赎回/购买开关  
> 购买token接口  
> 赎回token接口  
> ERC20查询到的账户余额为总余额   
> ERC20 transfer 可以将到期的锁定期余额转为可用余额  
> ERC20 transfer 可以实现token赎回功能  
> ERC20 transfer 可以实现冻结账户的罚款功能  
> 查询可用余额, 锁定余额，锁定期功能  
  
sht token 合约接口:  
> function totalSupply() public view returns (uint256);  
> function balanceOf(address who) public view returns (uint256);  
> function transfer(address to, uint256 value) public returns (bool);  
> function allowance(address owner, address spender) public view returns (uint256);  
> function transferFrom(address from, address to, uint256 value) public returns (bool);  
> function approve(address spender, uint256 value) public returns (bool);  
> function increaseApproval(address _spender, uint _addedValue) public returns (bool);  
> function decreaseApproval(address _spender, uint _subtractedValue) public returns (bool);  
> function pause() public;  
> function unpause() public;  
> function froze(address who) public;  
> function unfroze(address who) public;  
> function addAdministrator(address who) public;  
> function delAdministrator(address who) public;  
> function withdraw() public;  
> function batchTransfer(address[] _receivers, uint256[] _values) public;  
> function batchTransferFrom(address _from, address[] _receivers, uint256[] _values) public;  
> function transferByDate(address _receiver, uint256[] _values, uint256[] _dates) public;  
> function transferFromByDate(address _from, address _receiver, uint256[] _values, uint256[] _dates) public;  
> function addTokenToFund(address _from, uint256 _value);
> function buy() public payable;  
> function sell(uint256 _value) public;  
> function setSellPrice(uint256 price) public;  
> function setBuyPrice(uint256 price) public;  
> function openBuy() public;  
> function closeBuy() public;  
> function openSell() public;  
> function closeSell() public;  
> function availableBalancesOf(address _who) public;  
> function lockedBalanceOf(address _who) public;  
> function lockedBalancesOfByDate(address _who, uint256 date) public;  
  
2. 根据合约接口，写测试用例  
参照test/sample.js 编写测试用例  
  
3. 测试用例需要的模块如下:  
$ npm init  
$ npm install --save pify  
$ npm install --save log4js  
  
4. 根据合约接口，实现合约内容  
参照contracts/SibbayHealthToken.sol 编写合约  

