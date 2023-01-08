from flask_login import UserMixin
from sqlalchemy import String, Integer, Column

from src.models import BaseClass
from src.core.roles import ROLES


class User(UserMixin, BaseClass):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False, unique=False)

    car_registration = Column(String(10), nullable=False, unique=True)

    # roles: user: 0, admin: 1
    role = Column(Integer, nullable=False, unique=False)

    def __init__(self, name: str, email: str, password: str, car_registration: str, role: int = 0):
        self.name = name
        self.email = email
        self.password = password
        self.car_registration = car_registration
        self.role = role

    def __repr__(self):
        role_values = {value: key for key, value in ROLES.items()}
        return f'User(id={self.id}, name={self.name}, email={self.email}, ' \
               f'role={role_values[self.role]}, registration={self.car_registration})'
