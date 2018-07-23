import time

from mongoengine import (
    StringField,
    IntField,
    DecimalField,
)

from .base import Base


class TokenPrice(Base):
    """
    sibbay token 的 token_price
    """

    meta = {
        'db_alias': 'sht',
        'collection': 'token_price'
    }

    ether_price = DecimalField(required=True)
    ether_decimals = IntField(required=True)

    sht_price = DecimalField(required=True)
    sht_decimals = IntField(required=True)

    # 价格单位，代表该条记录 sht_price 和 ether_price 的单位，比如 USD CNY
    price_unit = StringField(required=True)

    created_at = IntField(required=True, default=time.time)

    @classmethod
    def query_latest_price(cls, *args, **kwargs):
        """
        query the latest price document
        return success and record
        """
        query = cls.objects(*args, **kwargs).order_by("-created_at")
        count = query.count()
        if count > 0:
            return (1, query.first())
        else:
            return (0, None)
