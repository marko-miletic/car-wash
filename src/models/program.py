from sqlalchemy import Integer, Column, ForeignKey

from src.models import BaseClass


class Program(BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    mode_id = Column(Integer, ForeignKey('mode.id'))

    def __init__(self, user_id: int, mode_id: int):
        self.user_id = user_id
        self.mode_id = mode_id

    def __repr__(self):
        return f'Program(id={self.id}, user_id={self.user_id}, mode_id={self.mode_id})'
