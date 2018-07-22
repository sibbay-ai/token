import time

from mongoengine import (
    StringField,
    IntField,
)

from .base import Base


class TokenTransfer(Base):
    """
    sibbay token 的 Transfer event
    """

    meta = {
        'db_alias': 'sht',
        'collection': 'token_transfer'
    }

    from_address = StringField(required=True)
    to_address = StringField(required=True)

    # value 设置为字符串的原因是：mongo 不支持 2 ** 256 - 1 这么大的整数
    # 所以需要转换成字符串保存
    value = StringField(required=True)

    transaction_hash = StringField(required=True)
    block_hash = StringField(required=True)
    block_number = IntField(required=True)

    created_at = IntField(required=True, default=time.time)
