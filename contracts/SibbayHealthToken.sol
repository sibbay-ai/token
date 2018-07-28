pragma solidity ^0.4.24;


import "./ManagementToken.sol";


/**
 * @title SibbayHealthToken
 */
contract SibbayHealthToken is StandardToken, Management {

  string public constant name = "Sibbay Health Token"; // solium-disable-line uppercase
  string public constant symbol = "SHT"; // solium-disable-line uppercase
  uint8 public constant decimals = 18; // solium-disable-line uppercase

  uint256 public constant INITIAL_SUPPLY = 1000000000 * (10 ** uint256(decimals));

  /**
   * 账户
   * availableBalances 可用余额
   * lockedBalances 锁定期余额
   * start_date 锁定期最早到期时间
   * end_date 锁定期最晚到期时间
   * */
  struct Account {
      uint256 availableBalances;
      mapping(uint32 => uint256) lockedBalances;
      uint32 start_date;
      uint32 end_date;
  }

  /**
   * 所有账户
   * */
  mapping(address => Account) accounts;

  /**
   * token 赎回价格
   * token 购买价格
   * 特殊资金账户，赎回token，接收购买token资金
   * 赎回购买标记
   * */
  uint256 sellPrice;
  uint256 buyPrice;
  address fundAccount;
  bool buySellFlag;

  /**
   * @dev Constructor that gives msg.sender all of existing tokens.
   */
  constructor() public {
    totalSupply_ = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
    emit Transfer(0x0, msg.sender, INITIAL_SUPPLY);
  }

  /**
   * modifier 要求开启购买赎回token
   * */
  modifier whenOpenBuySell()
  {
    require(buySellFlag);
  }

  /**
   * modifier 要求关闭购买赎回token
   * */
  modifier whenCloseBuySell()
  {
    require(!buySellFlag);
  }

  /**
   * TODO: 获取到期的锁定期余额
   * */
  function getLockedBalances() public
  {
  }

  /**
   * 可用余额转账，内部接口
   * */
  function transferAvailableBalances(
    address _to,
    uint256 _value,
  )
    internal
  {
    // 检查可用余额
    require(_value <= accounts[msg.sender].availableBalances)

    // 修改可用余额
    accounts[msg.sender].availableBalances = accounts[msg.sender].availableBalances.sub(_value);
    accounts[_to].availableBalances = accounts[_to].availableBalances.sub(_value);
  }

  /**
   * TODO:
   * 回传以太币, 内部接口
   * _from token来源账户
   * _to token目标账户
   * _value 为token数目
   * */
  function transferEther(
    address _from,
    address _to,
    address _value
  )
    internal
  {
  }

  /**
   * 转账
   * */
  function transfer(
    address _to,
    uint256 _value
  )
    public
    whenNotPaused
    whenNotFrozen(msg.sender)
    whenNotFrozen(_to)
    returns (bool)
  {
    /**
     * TODO: 获取到期的锁定期余额
     * */
    getLockedBalances();

    // 修改可用账户余额
    transferAvailableBalances(_to, _value);

    // 修改总账户余额
    super.transfer(_to, _value);

    // 回传以太币
    transferEther(msg.sender, _to, _value);

    return true;
  }

  /**
   * 代理转账
   * 代理从 _from 转账 _value 到 _to
   * */
  function transferFrom(
    address _from,
    address _to,
    uint256 _value
  )
    public
    whenNotPaused
    whenNotFrozen(msg.sender)
    whenNotFrozen(_from)
    whenNotFrozen(_to)
    returns (bool)
  {
    /**
     * TODO: 获取到期的锁定期余额
     * */
    getLockedBalances();

    // 修改可用账户余额
    transferAvailableBalances(_to, _value);

    // 修改总账户余额
    super.transferFrom(_from, _to, _value);

    //  回传以太币
    transferEther(_from, _to, _value);

    return true;
  }

  /**
   * 设定代理和代理额度
   * 设定代理为 _spender 额度为 _value
   * */
  function approve(
    address _spender,
    uint256 _value
  )
    public
    whenNotPaused
    whenNotFrozen(msg.sender)
    whenNotFrozen(_spender)
    returns (bool)
  {
    return super.approve(_spender, _value);
  }

  /**
   * 提高代理的代理额度
   * 提高代理 _spender 的代理额度 _addedValue
   * */
  function increaseApproval(
    address _spender,
    uint _addedValue
  )
    public
    whenNotPaused
    whenNotFrozen(msg.sender)
    whenNotFrozen(_spender)
    returns (bool success)
  {
    return super.increaseApproval(_spender, _addedValue);
  }

  /**
   * 降低代理的代理额度
   * 降低代理 _spender 的代理额度 _subtractedValue
   * */
  function decreaseApproval(
    address _spender,
    uint _subtractedValue
  )
    public
    whenNotPaused
    whenNotFrozen(msg.sender)
    whenNotFrozen(_spender)
    returns (bool success)
  {
    return super.decreaseApproval(_spender, _subtractedValue);
  }

  /**
   * 批量转账 token
   * 批量用户 _receivers
   * 对应的转账数量 _values
   * */
  function batchTransfer(
    address[] _receivers,
    uint256[] _values
  )
    public
    whenNotPaused
    whenNotFrozen(msg.sender)
  {
    // 判断接收账号和token数量为一一对应
    require(_receivers.length > 0 && _receivers.length == _values.length);

    /**
     * TODO: 获取到期的锁定期余额
     * */
    getLockedBalances();

    // 判断可用余额足够
    uint256 total = 0;
    for (uint32 i = 0; i < _values.length; i ++)
    {
      total = total.add(_values[i]);
    }
    require(total <= accounts[msg.sender].availableBalances)

    // 一一 转账
    for (uint32 i = 0; i < _receivers.length; i ++)
    {
      // 修改可用账户余额
      transferAvailableBalances(_receivers[i], _values[i]);

      // 修改总账户余额
      super.transfer(_receivers[i], _values[i]);

      //  回传以太币
      transferEther(msg.sender, _receivers[i], _values[i]);
    }
  }

  /**
   * TODO:
   * buy tokens
   * */
  function buy()
    public
    whenOpenBuySell
    payable
  {
  }

  /**
   * TODO:
   * sell tokens
   * */
  function sell(uint256 _value)
    public
    whenOpenBuySell
  {
  }

  /**
   * TODO:
   * 设置token赎回价格
   * */
  function setSellPrice(uint256 price)
    public
    whenAdministrator(msg.sender)
  {
    require(price > 0);
    sellPrice = price;
  }

  /**
   * TODO:
   * 设置token购买价格
   * */
  function setBuyPrice(uint256 price)
    public
    whenAdministrator(msg.sender)
  {
    require(price > 0);
    buyPrice = price;
  }

  /**
   * TODO:
   * 设置特殊资金账户
   * */
  function setBuyPrice(address fund)
    public
    whenAdministrator(msg.sender)
  {
    require(fund != address(0));
    fundAccount = fund;
  }

  /**
   * TODO:
   * 开启购买赎回token
   * */
  function openBuySell()
    public
    whenCloseBuySell
    onlyOwner
  {
    buySellFlag = true;
  }

  /**
   * TODO:
   * 关闭购买赎回token
   * */
  function closeBuySell()
    public
    whenOpenBuySell
    onlyOwner
  {
    buySellFlag = false;
  }

}
