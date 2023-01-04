from datetime import datetime
from sqlalchemy import String, Integer, Float, Column, DateTime

from src.models import BaseClass


class Discount(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    base_discount = Column(Integer, nullable=False, unique=False)
    additional_discount = Column(Integer, nullable=False, unique=False)
    additional_discount_description = Column(String(150), nullable=False, unique=False)

    valid_since = Column(DateTime, nullable=False, unique=False)

    def __init__(self, base_discount: int, additional_discount: int, additional_discount_description: int):
        self.base_discount = base_discount
        self.additional_discount = additional_discount
        self.additional_discount_description = additional_discount_description
        self.valid_since = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return f'Discount(id={self.id}, base_discount={self.base_discount}, ' \
               f'additional_discount={self.additional_discount}, ' \
               f'additional_discount_description={self.additional_discount_description}, ' \
               f'valid_since={self.valid_since})'
