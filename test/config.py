
import sys
sys.path.append("../sht_server")
import settings

# 所有测试一账户 [1-9]，密码均为123456
# 其中最后两个有其它的用途
accounts = ["0x0000000000000000000000000000000000000000", "0x2c67d7b6a2ba48b7228abc0b83c385ecf36d03a9", "0x748877b6ab98d6eef1335569364b28ac17f9c8e2", "0xcaa1f8bfb201a3d3692d0738ba12adec6c5bcc74", "0x123f2cf05824597894639631d5ca0cf71b1a4d23", "0x62e3368b9b60044ee97a47fd60abaa02b2c04326", "0x49ab59ae333c72d2cd23c31e4420017887a6b9d0", "0xe4e259e70d4bbe9c581bfc3847368f7984a9a4c5", "0x424679a12dc215aaf4d91b2770a70c1a050f5eab", "0x9e8e4da3982934eb6ceded360070eff92419e21a"]
password = "123456"
# 赎回地址账户
fund_account = accounts[len(accounts) - 1]
# 回收token账户
collect_account = accounts[len(accounts) - 2]

# gas, gas price
gas = 6000000
gas_price = 4000000000

# 1 token的最小单位
magnitude = 10**(settings.SIBBAY_SHT_DECIMALS)

# 交易等待确认时间
waitting_time = 10
