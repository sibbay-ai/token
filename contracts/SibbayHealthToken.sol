pragma solidity ^0.4.24;


import "./StandardToken.sol";
import "./Management.sol";


/**
 * @title SibbayHealthToken
 */
contract SibbayHealthToken is StandardToken, Management {

  string public constant name = "Sibbay Health Token"; // solium-disable-line uppercase
  string public constant symbol = "SHT"; // solium-disable-line uppercase
  uint8 public constant decimals = 18; // solium-disable-line uppercase

  uint256 public constant INITIAL_SUPPLY = 1000000000 * (10 ** uint256(decimals));

  // 事件
  event TransferEther(
    address indexed from,
    address indexed to,
    uint256 token_value,
    uint256 ether_value);

  /**
   * 将锁定期的map做成一个list
   * value 锁定的余额
   * _next 下个锁定期的到期时间
   * */
  struct Element {
    uint256 value;
    uint32 next;
  }

  /**
   * 账户
   * availableBalances 可用余额
   * lockedElement 锁定期余额
   * start_date 锁定期最早到期时间
   * end_date 锁定期最晚到期时间
   * */
  struct Account {
      uint256 availableBalances;
      mapping(uint32 => Element) lockedElement;
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
   * 常量
   * 单位量
   * */
  uint256 constant internal magnitude = 10 ** uint256(decimals);

  /**
   * 合约构造函数
   * 初始化合约的总供应量
   */
  constructor() public {
    totalSupply_ = INITIAL_SUPPLY;
    balances[msg.sender] = INITIAL_SUPPLY;
    accounts[msg.sender].availableBalances = INITIAL_SUPPLY;
    emit Transfer(0x0, msg.sender, INITIAL_SUPPLY);

    /**
     * 初始化合约属性
     * 赎回价格
     * 购买价格
     * 特殊资金账户
     * 赎回购买标记为false
     * */
    sellPrice = 0;
    buyPrice = 0;
    fundAccount = address(0);
    buySellFlag = false;
  }

  /**
   * modifier 要求开启购买赎回token
   * */
  modifier whenOpenBuySell()
  {
    require(buySellFlag);
    _;
  }

  /**
   * modifier 要求关闭购买赎回token
   * */
  modifier whenCloseBuySell()
  {
    require(!buySellFlag);
    _;
  }

  /**
   * 获取到期的锁定期余额, 内部接口
   * who: 账户地址
   * */
  function getlockedBalances(address who) internal
  {
    uint32 tmp_date;
    while(accounts[who].start_date != 0 &&
          accounts[who].start_date < now)
    {
        accounts[who].availableBalances = accounts[who].availableBalances.add(accounts[who].lockedElement[accounts[who].start_date].value);
        tmp_date = accounts[who].start_date;
        accounts[who].start_date = accounts[who].lockedElement[accounts[who].start_date].next;
        delete accounts[who].lockedElement[tmp_date];
    }

    if (accounts[who].start_date == 0)
        accounts[who].end_date = 0;
  }

  /**
   * 可用余额转账，内部接口
   * _from token的拥有者
   * _to token的接受者
   * _value token的数量
   * */
  function transferAvailableBalances(
    address _from,
    address _to,
    uint256 _value
  )
    internal
  {
    // 检查可用余额
    require(_value <= accounts[_from].availableBalances);

    // 修改可用余额
    accounts[_from].availableBalances = accounts[_from].availableBalances.sub(_value);
    accounts[_to].availableBalances = accounts[_to].availableBalances.add(_value);
  }

  /**
   * 回传以太币, 内部接口
   * _from token来源账户
   * _to token目标账户
   * _value 为token数目
   * */
  function transferEther(
    address _from,
    address _to,
    uint256 _value
  )
    internal
  {
    /**
     * 要求 _to 账户接收地址为特殊账户地址
     * */
    if (_to != fundAccount)
        return;

    /**
     * 没有开放赎回功能，直接返回
     * 这里不能用require，因为require会导致调用该函数的正常交易失败
     * */
    if (!buySellFlag)
      return;

    /**
     * 赎回价格必须大于0
     * 赎回的token必须大于0
     * */
    require(sellPrice > 0);
    require(_value > 0);

    // 赎回的以太币必须小于账户余额
    uint256 evalue = _value.mul(sellPrice).div(magnitude);
    require(evalue <= address(this).balance);

    // 回传以太币
    if (evalue > 0)
    {
      _from.transfer(evalue);
      emit TransferEther(_from, _to, _value, evalue);
    }
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
    getlockedBalances(msg.sender);

    // 修改可用账户余额
    transferAvailableBalances(msg.sender, _to, _value);

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
     * 获取到期的锁定期余额
     * */
    getlockedBalances(_from);

    // 修改可用账户余额
    transferAvailableBalances(_from, _to, _value);

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
     * 获取到期的锁定期余额
     * */
    getlockedBalances(msg.sender);

    // 判断可用余额足够
    uint32 i = 0;
    uint256 total = 0;
    for (i = 0; i < _values.length; i ++)
    {
      total = total.add(_values[i]);
    }
    require(total <= accounts[msg.sender].availableBalances);

    // 一一 转账
    for (i = 0; i < _receivers.length; i ++)
    {
      // 修改可用账户余额
      transferAvailableBalances(msg.sender, _receivers[i], _values[i]);

      // 修改总账户余额
      super.transfer(_receivers[i], _values[i]);

      //  回传以太币
      transferEther(msg.sender, _receivers[i], _values[i]);
    }
  }

  /**
   * 带有锁定期的转账, 当锁定期到期之后，锁定token数量将转入可用余额
   * _receivers 转账接收账户
   * _values 转账数量
   * _dates 锁定期，即到期时间
   * */
  function transferByDate(
    address[] _receivers,
    uint256[] _values,
    uint32[] _dates
  )
    public
    whenNotPaused
    whenNotFrozen(msg.sender)
  {
    // 判断接收账号和token数量为一一对应
    require(_receivers.length > 0 &&
        _receivers.length == _values.length &&
        _receivers.length == _values.length);

    /**
     * 获取到期的锁定期余额
     * */
    getlockedBalances(msg.sender);

    // 判断可用余额足够
    uint32 i = 0;
    uint256 total = 0;
    for (i = 0; i < _values.length; i ++)
    {
      total = total.add(_values[i]);
    }
    require(total <= accounts[msg.sender].availableBalances);

    // 转账
    for(i = 0; i < _receivers.length; i ++)
    {
      transferByDateSingle(_receivers[i], _values[i], _dates[i]);
    }
  }

  /**
   * */
  function transferByDateSingle(
    address _to,
    uint256 _value,
    uint32 _date
  )
    internal
  {
    /**
     * 到期时间比当前早，直接转入可用余额
     * */
    if (_date <= now)
    {
      // 修改可用账户余额
      transferAvailableBalances(msg.sender, _to, _value);

      // 修改总账户余额
      super.transfer(_to, _value);

      //  回传以太币
      transferEther(msg.sender, _to, _value);

      return ;
    }

    // 还没有收到过锁定期转账
    if (accounts[_to].start_date == 0)
    {
      // 最早时间和最晚时间一样
      accounts[_to].start_date = _date;
      accounts[_to].end_date = _date;
      accounts[_to].lockedElement[_date].value = _value;

      // 修改总账户余额
      super.transfer(_to, _value);

      return ;
    }

    // 锁定期比最早到期的还早
    if (_date < accounts[_to].start_date)
    {
      // 添加锁定期，并加入到锁定期列表
      accounts[_to].lockedElement[_date].value = _value;
      accounts[_to].lockedElement[_date].next = accounts[_to].start_date;
      accounts[_to].start_date = _date;

      // 修改总账户余额
      super.transfer(_to, _value);

      return ;
    }

    // 锁定期比最晚到期还晚
    if (_date > accounts[_to].end_date)
    {
        accounts[_to].lockedElement[_date].value = _value;
        accounts[_to].lockedElement[accounts[_to].end_date].next = _date;
        accounts[_to].end_date = _date;

      // 修改总账户余额
      super.transfer(_to, _value);

      return ;
    }

    /**
     * 锁定期在 最早和最晚之间
     * 首先找到插入的位置
     * 然后再插入的位置插入数据
     * */
    uint32 tmp_date = accounts[_to].start_date;
    while(accounts[_to].lockedElement[tmp_date].next != 0 &&
          accounts[_to].lockedElement[tmp_date].next < _date)
    {
      tmp_date = accounts[_to].lockedElement[tmp_date].next;
    }
    if(tmp_date == _date)
    {
      accounts[_to].lockedElement[tmp_date].value = accounts[_to].lockedElement[tmp_date].value.add(_value);
    }
    else
    {
      accounts[_to].lockedElement[_date].value = _value;
      accounts[_to].lockedElement[_date].next = accounts[_to].lockedElement[tmp_date].next;
      accounts[_to].lockedElement[tmp_date].next = _date;
    }

    // 修改总账户余额
    super.transfer(_to, _value);

    return ;
  }

  /**
   * buy tokens
   * */
  function buy()
    public
    whenOpenBuySell
    payable
  {
    /**
     * 购买价格必须大于0
     * 购买的value必须大于0
     * */
    require(buyPrice > 0);
    require(msg.value > 0);

    // 购买的token数量必须小于账户余额
    uint256 tvalue = msg.value.mul(magnitude).div(buyPrice);
    require(tvalue <= accounts[fundAccount].availableBalances);

    // 回传token
    if (tvalue > 0)
    {
      // 修改可用余额
      //transferAvailableBalances(fundAccount, msg.sender, tvalue);
      accounts[fundAccount].availableBalances = accounts[fundAccount].availableBalances.sub(tvalue);
      accounts[msg.sender].availableBalances = accounts[msg.sender].availableBalances.add(tvalue);

      // 修改总余额
      balances[fundAccount] = balances[fundAccount].sub(tvalue);
      balances[msg.sender] = balances[msg.sender].add(tvalue);
      emit Transfer(fundAccount, msg.sender, tvalue);
    }
  }

  /**
   * sell tokens
   * */
  function sell(uint256 _value)
    public
    whenOpenBuySell
  {
    require(fundAccount != address(0));
    transfer(fundAccount, _value);
  }

  /**
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
   * 设置特殊资金账户
   * */
  function setFundAccount(address fund)
    public
    whenAdministrator(msg.sender)
  {
    require(fund != address(0));
    fundAccount = fund;
  }

  /**
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
