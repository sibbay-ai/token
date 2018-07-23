
from init_data import init_sht_price
from sht_server import SHTData
from sht_server import SHTClass
import settings

from mongoengine import connect

if __name__ == '__main__':
    connect(
            settings.SIBBAY_MONGODB_SHT_DB,
            alias=settings.SIBBAY_MONGODB_SHT_DB,
            host=settings.SIBBAY_MONGODB_SHT_HOST
    )

    init_sht_price()

    sht_data = SHTData(
        settings.SIBBAY_ETHER_PRICE,
        settings.SIBBAY_ETHER_DECIMALS,
        settings.SIBBAY_SHT_PRICE,
        settings.SIBBAY_SHT_DECIMALS
    )

    sc = SHTClass(
        settings.SIBBAY_SHT_OWNER,
        settings.SIBBAY_SHT_PASSWORD,
        settings.SIBBAY_SHT_GAS_PRICE,
        settings.SIBBAY_SHT_ADDRESS,
        settings.SIBBAY_SHT_ABI,
        sht_data,
        settings.SIBBAY_MONGODB_SHT_HOST
    )

    te = sc.start_price_thread(30)
    tw = sc.start_watch_sht_transfer(settings.SIBBAY_SHT_NODE_IPC, 5)
    tp = sc.start_pay_ether(settings.SIBBAY_SHT_NODE_IPC, 5)

    te.join()
    tw.join()
    tp.join()


