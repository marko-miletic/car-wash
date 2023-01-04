from src.database.session import SessionLocal, engine
from src.models import BaseClass


def init_db():
    session = SessionLocal()
    BaseClass.metadata.create_all(engine, checkfirst=True)
