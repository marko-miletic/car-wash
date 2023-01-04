from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import BaseClass
from .user import User
from .discount import Discount
from .invoice import Invoice
from .mode import Mode
from .program import Program

# dialect+driver://username:password@host:port/database

# Session = sessionmaker(db)
# session = Session()

# BaseClass.metadata.create_all(db, checkfirst=True)
