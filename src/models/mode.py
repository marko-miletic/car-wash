from sqlalchemy import String, Integer, Column, Boolean

from src.models import BaseClass


class Mode(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    description = Column(String(50), nullable=False, unique=True)
    price = Column(Integer, nullable=False, unique=False)
    active = Column(Boolean, nullable=False, unique=False)

    def __init__(self, description: str, price: int, active: bool = True):
        self.description = description
        self.price = price
        self.active = active

    def __repr__(self):
        return f'Mode(id={self.id}, description={self.description}, price={self.price}, active={self.active})'
