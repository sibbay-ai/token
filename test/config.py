
import sys
sys.path.append("../sht_server")
import settings

# 所有测试密码均为123456
accounts = ["0x0000000000000000000000000000000000000000"]
password = "123456"

# gas, gas price
gas = 6000000
gas_price = 4000000000

# 1 token的最小单位
magnitude = 10**(settings.SIBBAY_SHT_DECIMALS)

# 交易等待确认时间
waitting_time = 5
