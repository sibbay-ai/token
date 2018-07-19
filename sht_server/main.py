
from init_data import init_sht_price
import sht_server
from sht_server import SHTData
from sht_server import SHTClass
import settings

if __name__ == '__main__':
    init_sht_price()
    sht_data = SHTData(settings.SIBBAY_SHT_ETHER_PRICE, settings.SIBBAY_SHT_ETHER_DECIMALS, \
            settings.SIBBAY_SHT_SHT_PRICE, settings.SIBBAY_SHT_SHT_DECIMALS)
    sc = SHTClass(settings.SIBBAY_SHT_OWNER, settings.SIBBAY_SHT_PASSWORD, settings.sht_address, settings.sht_abi, sht_data, settings.SIBBAY_MONGODB_SHT_HOST)
    te = sc.start_price_thread(30)
    tq = sc.start_queue_thread(5)
    tw = sc.start_watch_sht_transfer(settings.SIBBAY_SHT_NODE_IPC, 5)
    tp = sc.start_pay_ether(settings.SIBBAY_SHT_NODE_IPC, 5)

    te.join()
    tq.join()
    tw.join()
    tp.join()


