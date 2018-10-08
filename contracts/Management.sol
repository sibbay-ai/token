pragma solidity ^0.4.24;


import "./Ownable.sol";


/**
 * 管理合约
 * 功能：
 * 暂停合约
 * 冻结账户
 * 管理员
 */
contract Management is Ownable {

  /**
   * 暂停和取消暂停事件
   * */
  event Pause();
  event Unpause();

  /**
   * 冻结和取消冻结事件
   * */
  event Froze(address indexed admin, address indexed who);
  event Unfroze(address indexed admin, address indexed who);

  /**
   * 增加和删除管理员事件
   * */
  event AddAdministrator(address indexed admin);
  event DelAdministrator(address indexed admin);

  /**
   * 合约暂停标志, True 暂停，false 未暂停
   * 合约冻结账户
   * 合约管理员
   * */
  bool public paused = false;
  mapping(address => bool) public frozenList;
  mapping(address => bool) public adminList;

  /**
   * 构造函数
   * 初始化owner是管理员
   * */
  constructor() public {
    adminList[owner] = true;
  }

  /**
   * modifier 要求合约正在运行状态
   */
  modifier whenNotPaused() {
    require(!paused);
    _;
  }

  /**
   * modifier 要求合约暂停状态
   */
  modifier whenPaused() {
    require(paused);
    _;
  }

  /**
   * modifier 要求账户未冻结状态
   * */
  modifier whenNotFrozen(address who) {
    require(!frozenList[who]);
    _;
  }

  /**
   * modifier 要求账户冻结状态
   * */
  modifier whenFrozen(address who) {
    require(frozenList[who]);
    _;
  }

  /**
   * 要求是管理员
   * */
  modifier whenAdministrator(address who) {
    require(adminList[who]);
    _;
  }

  /**
   * 要求不是管理员
   * */
  modifier whenNotAdministrator(address who) {
    require(!adminList[who]);
    _;
  }

  /**
   * * 暂停合约
   */
  function pause() onlyOwner whenNotPaused public {
    paused = true;
    emit Pause();
  }

  /**
   * 取消暂停合约
   */
  function unpause() onlyOwner whenPaused public {
    paused = false;
    emit Unpause();
  }

  /**
   * 冻结账户
   * */
  function froze(address who) whenAdministrator(msg.sender) public {
    frozenList[who] = true;
    emit Froze(msg.sender, who);
  }

  /**
   * 取消冻结账户
   * */
  function unfroze(address who) whenAdministrator(msg.sender) public {
    //不允许自己解冻,即使自己是admin
    require(who != msg.sender);

    delete frozenList[who];
    emit Unfroze(msg.sender, who);
  }

  /**
   * 添加管理员
   * */
  function addAdministrator(address who) onlyOwner public {
    adminList[who] = true;
    emit AddAdministrator(who);
  }

  /**
   * 删除管理员
   * */
  function delAdministrator(address who) onlyOwner public {
    delete adminList[who];
    emit DelAdministrator(who);
  }
}
