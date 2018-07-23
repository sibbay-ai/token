import time

from mongoengine import (
    StringField,
    IntField,
    DecimalField,
)

from .base import Base


class TokenSell(Base):
    """
    sibbay token 的 token_sell 记录
    """

    meta = {
        'db_alias': 'sht',
        'collection': 'token_sell'
    }

    from_address = StringField(required=True)
    to_address = StringField(required=True)

    # value 设置为字符串的原因是：mongo 不支持 2 ** 256 - 1 这么大的整数
    # 所以需要转换成字符串保存
    value = StringField(required=True)

    transaction_hash = StringField(required=True, unique=True)
    block_hash = StringField(required=True)
    block_number = IntField(required=True)

    # may set a reference field
    #tx_info = ReferenceField(TokenTransfer)

    sht_price = DecimalField(required=True)
    ether_price = DecimalField(required=True)

    # 价格单位，代表该条记录 sht_price 和 ether_price 的单位，比如 USD CNY
    price_unit = StringField(required=True)

    ether_hash = StringField()

    # value 设置为字符串的原因是：mongo 不支持 2 ** 256 - 1 这么大的整数
    # 所以需要转换成字符串保存
    ether_value = StringField(required=True)

    STATUS__INIT = "INIT"
    STATUS__PROCESSING = "PROCESSING"
    STATUS__PROCESSED = "PROCESSED"
    STATUS__FAILED = "FAILED"
    STATUS__MANUAL = "MANUAL"
    STATUS__SUCCESS = "SUCCESS"
    status = StringField(choices=(STATUS__INIT, STATUS__PROCESSING, STATUS__SUCCESS), default=STATUS__INIT)

    # 数据记录创建时间
    created_at = IntField(required=True, default=time.time)
    # 数据记录最后更新时间
    updated_at = IntField(required=True, default=time.time)
