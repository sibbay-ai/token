# function list

## 任何人都可以进行的查询
````
name
symbol
decimals
INITIAL_SUPPLY
totalSupply
owner
accounts
sellPrice
buyPrice
fundAccount
buySellFlag
allowance
paused
frozenList
adminList
getAvailableBalances
balanceOf
````

## 任何人都可以进行的写操作
当合约暂停时，不能使用
```
transfer
transferFrom
batchTransfer
batchTransferFrom
transferByDate
transferFromByDate
approve
increaseApproval
decreaseApproval
buy
sell
```

## 只有管理员和 onwer 可以进行的写操作
```
froze
unfroze
setSellPrice
setBuyPrice
```

## 只有 onwer 可以进行的写操作
```
setFundAccount
transferOwnership
renounceOwnership
withdraw
addAdministrator
delAdministrator
pause
unpause
openBuySell
closeBuySell
```