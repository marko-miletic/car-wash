from datetime import datetime
from sqlalchemy import Integer, Column, DateTime, ForeignKey, Boolean, Float

from src.models import BaseClass


class Invoice(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    price = Column(Float, nullable=False, unique=False)
    time_stamp = Column(DateTime, nullable=False, unique=True)

    completed = Column(Boolean, nullable=False, unique=False)

    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, price: float, user_id: int):
        self.price = price
        self.user_id = user_id
        self.time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.completed = False

    def __repr__(self):
        return f'Invoice(id={self.id}, price={self.price}, time={self.time_stamp},' \
               f'user_id={self.user_id}, completed={self.completed})'

