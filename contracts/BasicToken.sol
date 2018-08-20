pragma solidity ^0.4.24;


import "./ERC20Basic.sol";
import "./SafeMath.sol";


/**
 * ERC20 基类实现
 */
contract BasicToken is ERC20Basic {
  using SafeMath for uint256;

  /**
   * 账户总余额
   * */
  mapping(address => uint256) balances;

  /**
   * 总供应量
   * */
  uint256 totalSupply_;

  /**
   * 获取总供应量
   * */
  function totalSupply() public view returns (uint256) {
    return totalSupply_;
  }

  /**
   * 转账
   * _to token接收账户
   * _value token转账数量
   * */
  /* 注释掉这个接口，不在这里实现
  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);

    balances[msg.sender] = balances[msg.sender].sub(_value);
    balances[_to] = balances[_to].add(_value);
    emit Transfer(msg.sender, _to, _value);
    return true;
  }
  */

  /**
   * 查询账户总余额
   * */
  function balanceOf(address _owner) public view returns (uint256) {
    return balances[_owner];
  }

}
